"""
scorer.py — Multi-factor recipe scoring engine.
Scores recipes on: time fit, nutrition need, variety, family rating, pantry match.
"""

from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
import json
import os

MEAL_LOG_FILE = os.path.join(os.path.dirname(__file__), "meal_log.json")

WEIGHTS = {
    "time_fit": 0.15,
    "nutrition": 0.25,
    "variety": 0.20,
    "rating": 0.25,
    "pantry": 0.15,
}


def load_meal_log() -> List[Dict]:
    """Load meal log from JSON file."""
    if os.path.exists(MEAL_LOG_FILE):
        with open(MEAL_LOG_FILE, "r") as f:
            return json.load(f)
    return []


def save_meal_log(log: List[Dict]):
    """Save meal log to JSON file."""
    with open(MEAL_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def log_meal(recipe_name: str, protein: int, fiber: int, calories: int):
    """Record a meal."""
    log = load_meal_log()
    log.append({
        "date": date.today().isoformat(),
        "recipe": recipe_name,
        "protein_g": protein,
        "fiber_g": fiber,
        "calories": calories,
    })
    save_meal_log(log)


def get_weekly_nutrition(log: List[Dict] = None) -> Dict[str, int]:
    """Sum this week's nutrition from the log."""
    log = log or load_meal_log()
    week_start = date.today() - timedelta(days=date.today().weekday())
    totals = {"protein": 0, "fiber": 0, "calories": 0}
    for entry in log:
        entry_date = date.fromisoformat(entry["date"])
        if entry_date >= week_start:
            totals["protein"] += entry.get("protein_g", 0)
            totals["fiber"] += entry.get("fiber_g", 0)
            totals["calories"] += entry.get("calories", 0)
    return totals


def get_recent_recipes(log: List[Dict] = None, days: int = 3) -> List[str]:
    """Get recipe names cooked in the last N days."""
    log = log or load_meal_log()
    cutoff = date.today() - timedelta(days=days)
    return [
        entry["recipe"]
        for entry in log
        if date.fromisoformat(entry["date"]) >= cutoff
    ]


def score_recipes(
    recipes: List[Dict],
    available_minutes: int,
    pantry: Dict[str, bool],
    goals: Dict[str, int],
    boost: str = None,
) -> List[Dict]:
    """
    Score and rank all recipes. Returns sorted list of:
    {recipe, score, scores, reasons}
    """
    log = load_meal_log()
    weekly = get_weekly_nutrition(log)
    recent = get_recent_recipes(log)

    # Find biggest nutrition gap
    protein_pct = (weekly["protein"] / goals["protein"] * 100) if goals["protein"] else 100
    fiber_pct = (weekly["fiber"] / goals["fiber"] * 100) if goals["fiber"] else 100
    biggest_gap = "protein" if protein_pct <= fiber_pct else "fiber"
    biggest_gap_pct = min(protein_pct, fiber_pct)

    weights = dict(WEIGHTS)
    if boost == "protein":
        weights["nutrition"] = 0.40
        weights["rating"] = 0.10
    elif boost == "quick":
        weights["time_fit"] = 0.35
        weights["variety"] = 0.10
    elif boost == "pantry":
        weights["pantry"] = 0.35
        weights["nutrition"] = 0.10
    elif boost == "comfort":
        weights["rating"] = 0.40
        weights["variety"] = 0.10

    results = []
    for recipe in recipes:
        # Hard filter: must fit in available time
        if recipe["total_minutes"] > available_minutes:
            continue

        scores = {}
        reasons = []

        # 1. Time fit
        scores["time_fit"] = min(1.0, (available_minutes - recipe["total_minutes"]) / max(available_minutes, 1) + 0.3)
        reasons.append(f"⏱️ {recipe['total_minutes']} min (you have {available_minutes})")

        # 2. Nutrition gap fill
        if biggest_gap == "protein":
            scores["nutrition"] = min(1.0, recipe["protein_g"] / 24 * 1.5)  # 24g = great
            if scores["nutrition"] > 0.6:
                reasons.append(f"💪 Great protein: {recipe['protein_g']}g (you're at {protein_pct:.0f}% this week)")
        else:
            scores["nutrition"] = min(1.0, recipe["fiber_g"] / 14 * 1.5)  # 14g = great
            if scores["nutrition"] > 0.6:
                reasons.append(f"🥬 Great fiber: {recipe['fiber_g']}g (you're at {fiber_pct:.0f}% this week)")

        # 3. Variety (penalize recently cooked)
        if recipe["name"] in recent:
            scores["variety"] = 0.05
            reasons.append("⚠️ Had this recently")
        else:
            scores["variety"] = 0.85

        # 4. Family rating
        scores["rating"] = recipe["family_rating"] / 5.0
        if recipe["family_rating"] >= 5:
            reasons.append("⭐ Family favorite!")

        # 5. Pantry match
        ingredients = recipe.get("key_ingredients", [])
        if ingredients:
            matched = sum(1 for ing in ingredients if _pantry_has(ing, pantry))
            scores["pantry"] = matched / len(ingredients)
            missing = [ing for ing in ingredients if not _pantry_has(ing, pantry)]
            if missing:
                reasons.append(f"🛒 Need: {', '.join(missing[:3])}")
            else:
                reasons.append("✅ All ingredients on hand")
        else:
            scores["pantry"] = 0.5

        # Weighted total
        total = sum(scores[k] * weights.get(k, 0) for k in scores)

        results.append({
            "recipe": recipe,
            "score": round(total * 100),
            "scores": {k: round(v * 100) for k, v in scores.items()},
            "reasons": reasons,
        })

    results.sort(key=lambda x: -x["score"])
    return results


def format_recommendation(result: Dict, rank: int = 1) -> str:
    """Format a recommendation as a Teams-friendly message."""
    r = result["recipe"]
    medal = ["🥇", "🥈", "🥉"][min(rank - 1, 2)]
    lines = [
        f"{medal} **{r['name']}**",
        f"{r['cuisine']} · {r['difficulty']} · {r['total_minutes']} min · ⭐ {r['family_rating']}/5",
        f"Score: **{result['score']}%**",
        "",
    ]
    for reason in result["reasons"]:
        lines.append(f"  {reason}")
    lines.append(f"\n  *P:{r['protein_g']}g · Fiber:{r['fiber_g']}g · {r['calories']}cal*")
    return "\n".join(lines)


def nutrition_summary() -> str:
    """Return a formatted weekly nutrition summary."""
    weekly = get_weekly_nutrition()
    goals = {"protein": 400, "fiber": 175, "calories": 14000}
    log = load_meal_log()
    week_start = date.today() - timedelta(days=date.today().weekday())
    meals = [e for e in log if date.fromisoformat(e["date"]) >= week_start]

    p_pct = round(weekly["protein"] / goals["protein"] * 100) if goals["protein"] else 0
    f_pct = round(weekly["fiber"] / goals["fiber"] * 100) if goals["fiber"] else 0
    c_pct = round(weekly["calories"] / goals["calories"] * 100) if goals["calories"] else 0

    lines = [
        f"📊 **This week** ({len(meals)} meals logged):",
        f"  💪 Protein: {weekly['protein']}g / {goals['protein']}g ({p_pct}%)",
        f"  🥬 Fiber: {weekly['fiber']}g / {goals['fiber']}g ({f_pct}%)",
        f"  🔥 Calories: {weekly['calories']} / {goals['calories']} ({c_pct}%)",
    ]
    if p_pct < 30:
        lines.append(f"\n⚠️ Protein is low at {p_pct}% — prioritizing high-protein recipes.")
    elif f_pct < 30:
        lines.append(f"\n⚠️ Fiber is low at {f_pct}% — prioritizing high-fiber recipes.")
    else:
        lines.append("\n✅ On track!")
    return "\n".join(lines)


def _pantry_has(ingredient: str, pantry: Dict[str, bool]) -> bool:
    """Check if an ingredient is in the pantry (fuzzy match)."""
    ing = ingredient.lower().strip()
    for item, in_stock in pantry.items():
        if not in_stock:
            continue
        if ing in item or item in ing:
            return True
        # Check key word overlap
        ing_words = set(ing.split())
        item_words = set(item.split())
        if any(w in item_words for w in ing_words if len(w) > 3):
            return True
    return False
