"""
notify.py — RecipeBot CLI + Desktop Notifications.

Usage:
  python notify.py dinner                        # What's for dinner? (default 90 min)
  python notify.py dinner --time 30              # Quick meal
  python notify.py dinner --boost protein        # Prioritize protein
  python notify.py dinner --ics "https://..."    # Use real calendar

  python notify.py log "Dal Tadka"               # Log tonight's dinner
  python notify.py log "Palak Paneer" --notes "With naan"

  python notify.py pantry                        # Show pantry
  python notify.py pantry add "spinach, tofu"    # Mark items as in-stock
  python notify.py pantry remove "paneer"        # Mark items as out-of-stock

  python notify.py nutrition                     # Weekly nutrition summary
  python notify.py meals                         # Recent meal log
"""

import argparse
import os
import sys
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import recipes as recipe_data
import scorer
import calendar_ics as cal_ics
from plyer import notification

RECIPES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recipes.txt")


def cmd_dinner(args):
    """What's for dinner?"""
    all_recipes = recipe_data.load_recipes()
    pantry = recipe_data.load_pantry()
    goals = recipe_data.load_nutrition_goals()

    # Calendar
    ics_url = args.ics or _get_config_ics()
    if ics_url:
        free_minutes, cal_summary = cal_ics.get_cooking_window(ics_url)
    else:
        free_minutes = args.time
        cal_summary = f"{free_minutes} min free tonight"

    results = scorer.score_recipes(all_recipes, free_minutes, pantry, goals, args.boost)

    if not results:
        msg = f"No recipes fit a {free_minutes}-min window!"
        print(f"\n😅 {msg}")
        notification.notify(title="🍳 RecipeBot", message=msg, timeout=10)
        return

    # Print top 3
    print(f"\n📅 {cal_summary}")
    print(scorer.nutrition_summary())
    print("\n" + "─" * 50)
    print("🍳 TONIGHT'S PICKS:\n")

    for i, result in enumerate(results[:3]):
        r = result["recipe"]
        medal = ["🥇", "🥈", "🥉"][i]
        print(f"  {medal} {r['name']}")
        print(f"     {r['cuisine']} · {r['total_minutes']} min · ⭐ {r['family_rating']}/5 · Match: {result['score']}%")
        for reason in result["reasons"]:
            print(f"     {reason}")
        print(f"     P:{r['protein_g']}g · Fiber:{r['fiber_g']}g · {r['calories']}cal")
        print()

    # Desktop notification for #1
    top = results[0]["recipe"]
    notification.notify(
        title=f"🍳 Tonight: {top['name']}",
        message=f"{top['cuisine']} · {top['total_minutes']} min · ⭐ {top['family_rating']}/5\n"
                f"Match: {results[0]['score']}% · P:{top['protein_g']}g\n"
                f"{cal_summary}",
        timeout=15,
        app_name="RecipeBot",
    )

    print(f"💡 To log: python notify.py log \"{top['name']}\"")


def cmd_log(args):
    """Log tonight's dinner."""
    all_recipes = recipe_data.load_recipes()
    name = args.recipe

    # Fuzzy match recipe name
    matched = None
    for recipe in all_recipes:
        if recipe["name"].lower() == name.lower():
            matched = recipe
            break
    if not matched:
        # Partial match
        for recipe in all_recipes:
            if name.lower() in recipe["name"].lower():
                matched = recipe
                break

    if matched:
        scorer.log_meal(matched["name"], matched["protein_g"], matched["fiber_g"], matched["calories"])
        weekly = scorer.get_weekly_nutrition()
        goals = recipe_data.load_nutrition_goals()
        p_pct = round(weekly["protein"] / goals["protein"] * 100)

        print(f"\n✅ Logged: {matched['name']}")
        print(f"   +{matched['protein_g']}g protein · +{matched['fiber_g']}g fiber · +{matched['calories']} cal")
        print(f"   Protein this week: {weekly['protein']}g / {goals['protein']}g ({p_pct}%)")
        if args.notes:
            print(f"   Notes: {args.notes}")

        notification.notify(
            title=f"✅ Logged: {matched['name']}",
            message=f"+{matched['protein_g']}g protein · Protein now at {p_pct}%",
            timeout=5,
        )
    else:
        print(f"\n❌ Recipe not found: \"{name}\"")
        print("   Available recipes:")
        for r in sorted(all_recipes, key=lambda x: x["name"]):
            print(f"     - {r['name']}")


def cmd_pantry(args):
    """Show or manage pantry."""
    pantry = recipe_data.load_pantry()

    if args.action == "add":
        items = [i.strip().lower() for i in args.items.split(",")]
        _update_pantry_in_file(items, in_stock=True)
        print(f"\n✅ Marked as IN STOCK: {', '.join(items)}")

    elif args.action == "remove":
        items = [i.strip().lower() for i in args.items.split(",")]
        _update_pantry_in_file(items, in_stock=False)
        print(f"\n❌ Marked as NEED TO BUY: {', '.join(items)}")

    else:
        # Show pantry
        in_stock = sorted([k for k, v in pantry.items() if v])
        to_buy = sorted([k for k, v in pantry.items() if not v])
        print(f"\n🥫 PANTRY ({len(in_stock)} in stock)")
        print(f"   {', '.join(in_stock)}")
        print(f"\n🛒 NEED TO BUY ({len(to_buy)})")
        print(f"   {', '.join(to_buy)}")


def cmd_nutrition(args):
    """Weekly nutrition summary."""
    print(f"\n{scorer.nutrition_summary()}")


def cmd_meals(args):
    """Show recent meals."""
    from datetime import date, timedelta
    log = scorer.load_meal_log()
    week_start = date.today() - timedelta(days=date.today().weekday())
    recent = [e for e in log if date.fromisoformat(e["date"]) >= week_start]

    print(f"\n📅 MEALS THIS WEEK ({len(recent)} logged):\n")
    for m in recent:
        print(f"  {m['date']}  {m['recipe']:30s}  P:{m['protein_g']}g  Fiber:{m['fiber_g']}g  {m['calories']}cal")

    if not recent:
        print("  (none logged yet)")


def _get_config_ics():
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if line.strip().startswith("ics="):
                    return line.strip().split("=", 1)[1]
    return None


def _update_pantry_in_file(items, in_stock=True):
    """Move items between 'Always stocked' and 'Usually need to buy' sections in recipes.txt."""
    with open(RECIPES_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for item in items:
        if in_stock:
            # Remove from "need to buy", add to "always stocked"
            content = re.sub(
                r"(### Usually need to buy:\n)(.*)",
                lambda m: m.group(1) + re.sub(rf",?\s*{re.escape(item)}", "", m.group(2)),
                content, flags=re.DOTALL
            )
            # Add to always stocked if not already there
            if item not in content.split("### Always stocked:")[1].split("### Usually")[0].lower():
                content = content.replace(
                    "### Always stocked:\n",
                    f"### Always stocked:\n{item}, "
                )
        else:
            # Remove from "always stocked", add to "need to buy"
            content = re.sub(
                r"(### Always stocked:\n)(.*?)(### Usually)",
                lambda m: m.group(1) + re.sub(rf",?\s*{re.escape(item)}", "", m.group(2)) + m.group(3),
                content, flags=re.DOTALL
            )
            if item not in content.split("### Usually need to buy:")[1].lower():
                content = content.replace(
                    "### Usually need to buy:\n",
                    f"### Usually need to buy:\n{item}, "
                )

    with open(RECIPES_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="🍳 RecipeBot — What's for dinner?",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python notify.py dinner                   What's for dinner tonight?
  python notify.py dinner --time 30         Quick meal under 30 min
  python notify.py dinner --boost protein   Prioritize protein
  python notify.py log "Dal Tadka"          Log what you cooked
  python notify.py pantry                   Show pantry inventory
  python notify.py pantry add "spinach"     Mark items in stock
  python notify.py pantry remove "paneer"   Mark items out of stock
  python notify.py nutrition                Weekly nutrition progress
  python notify.py meals                    This week's meal log
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # dinner
    p_dinner = sub.add_parser("dinner", help="Get tonight's recommendation")
    p_dinner.add_argument("--time", type=int, default=90, help="Available minutes (default: 90)")
    p_dinner.add_argument("--boost", choices=["protein", "fiber", "quick", "comfort", "pantry"])
    p_dinner.add_argument("--ics", type=str, default=None, help="Outlook ICS URL")

    # log
    p_log = sub.add_parser("log", help="Log a meal")
    p_log.add_argument("recipe", type=str, help="Recipe name (partial match OK)")
    p_log.add_argument("--notes", type=str, default="", help="Optional notes")

    # pantry
    p_pantry = sub.add_parser("pantry", help="View/manage pantry")
    p_pantry.add_argument("action", nargs="?", choices=["add", "remove"], default=None)
    p_pantry.add_argument("items", nargs="?", type=str, default="", help="Comma-separated items")

    # nutrition
    sub.add_parser("nutrition", help="Weekly nutrition summary")

    # meals
    sub.add_parser("meals", help="Recent meal log")

    args = parser.parse_args()

    if args.command == "dinner" or args.command is None:
        if args.command is None:
            args.time = 90
            args.boost = None
            args.ics = None
        cmd_dinner(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "pantry":
        cmd_pantry(args)
    elif args.command == "nutrition":
        cmd_nutrition(args)
    elif args.command == "meals":
        cmd_meals(args)


if __name__ == "__main__":
    main()
