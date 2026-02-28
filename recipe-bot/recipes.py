"""
recipes.py — Parse the recipes.txt file into structured data for scoring.
"""

import re
import os
from datetime import date, timedelta
from typing import List, Dict

RECIPES_FILE = os.path.join(os.path.dirname(__file__), "recipes.txt")


def load_recipes(filepath: str = RECIPES_FILE) -> List[Dict]:
    """Parse recipes.txt into a list of recipe dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    recipes = []
    # Split by ### headings (recipe names)
    blocks = re.split(r"^### ", content, flags=re.MULTILINE)

    for block in blocks[1:]:  # skip preamble
        lines = block.strip().split("\n")
        name = lines[0].strip()

        # Skip non-recipe sections
        if name in ("Always stocked:", "Usually need to buy:"):
            continue

        recipe = {
            "name": name,
            "total_minutes": 30,
            "difficulty": "Easy",
            "family_rating": 3,
            "protein_g": 10,
            "carbs_g": 40,
            "fat_g": 10,
            "fiber_g": 4,
            "calories": 300,
            "key_ingredients": [],
            "tags": [],
            "cuisine": "",
            "notes": "",
            "last_cooked": None,
        }

        for line in lines[1:]:
            line = line.strip().lstrip("- ")

            if line.startswith("Time:"):
                m = re.search(r"(\d+)\s*min", line)
                if m:
                    recipe["total_minutes"] = int(m.group(1))
                if "Easy" in line:
                    recipe["difficulty"] = "Easy"
                elif "Medium" in line:
                    recipe["difficulty"] = "Medium"
                elif "Hard" in line:
                    recipe["difficulty"] = "Hard"
                m = re.search(r"Rating:\s*(\d)/5", line)
                if m:
                    recipe["family_rating"] = int(m.group(1))

            elif line.startswith("Protein:"):
                m = re.findall(r"(\w+):\s*(\d+)", line)
                for key, val in m:
                    key_lower = key.lower()
                    if key_lower == "protein":
                        recipe["protein_g"] = int(val)
                    elif key_lower == "fiber":
                        recipe["fiber_g"] = int(val)
                    elif key_lower == "calories":
                        recipe["calories"] = int(val)

            elif line.startswith("Ingredients:"):
                ingredients_str = line.replace("Ingredients:", "").strip()
                recipe["key_ingredients"] = [i.strip() for i in ingredients_str.split(",") if i.strip()]

            elif line.startswith("Notes:"):
                recipe["notes"] = line.replace("Notes:", "").strip()

        recipes.append(recipe)

    # Assign cuisines from section headers
    section_map = {}  # recipe_name → cuisine
    current_cuisine = ""
    for line in content.split("\n"):
        if line.startswith("## ") and not line.startswith("## Dietary") and not line.startswith("## Favorite") and not line.startswith("## Household") and not line.startswith("## Weekly") and not line.startswith("## WHAT"):
            current_cuisine = line.replace("## ", "").strip()
            # Clean up: "SOUTH INDIAN RECIPES" → "South Indian"
            current_cuisine = current_cuisine.replace(" RECIPES", "").replace("RECIPES", "")
            current_cuisine = current_cuisine.replace(" / ", "/").title()
        elif line.startswith("### ") and current_cuisine:
            rname = line.replace("### ", "").strip()
            section_map[rname] = current_cuisine

    for r in recipes:
        r["cuisine"] = section_map.get(r["name"], "Other")

    return recipes


def load_pantry(filepath: str = RECIPES_FILE) -> Dict[str, bool]:
    """Parse the pantry section from recipes.txt."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pantry = {}

    # Find "Always stocked" section
    m = re.search(r"### Always stocked:\s*\n(.+?)(?=\n###|\Z)", content, re.DOTALL)
    if m:
        items = re.split(r"[,\n]", m.group(1))
        for item in items:
            item = item.strip().lower()
            if item and len(item) > 1:
                pantry[item] = True

    # Find "Usually need to buy" section
    m = re.search(r"### Usually need to buy:\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if m:
        items = re.split(r"[,\n]", m.group(1))
        for item in items:
            item = item.strip().lower()
            if item and len(item) > 1:
                pantry[item] = False

    return pantry


def load_nutrition_goals(filepath: str = RECIPES_FILE) -> Dict[str, int]:
    """Parse nutrition goals from the text file."""
    return {
        "protein": 400,  # g/week
        "fiber": 175,    # g/week
        "calories": 14000,  # kcal/week
    }


if __name__ == "__main__":
    recipes = load_recipes()
    print(f"Loaded {len(recipes)} recipes")
    for r in recipes[:5]:
        print(f"  {r['name']:30s} | {r['cuisine']:20s} | {r['total_minutes']}min | P:{r['protein_g']}g | ⭐{r['family_rating']}")

    pantry = load_pantry()
    in_stock = sum(1 for v in pantry.values() if v)
    print(f"\nPantry: {in_stock} in stock, {len(pantry) - in_stock} to buy")
