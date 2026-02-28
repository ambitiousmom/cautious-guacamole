"""
RecipeBot — Streamlit App (Claude-style UX)
Clean conversational interface with a side panel for context.
"""

import streamlit as st
from datetime import date, timedelta
import recipes as recipe_data
import scorer
import calendar_ics as cal_ics

# ─── Page Config ───
st.set_page_config(
    page_title="RecipeBot",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Claude-style CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:wght@400;600&display=swap');

/* Reset streamlit defaults */
#MainMenu, footer, .stDeployButton, header {display: none !important;}
.block-container {padding: 0 !important; max-width: 100% !important;}
section[data-testid="stSidebar"] {background: #f9f5f1;}

/* Color palette — warm Claude aesthetic */
:root {
    --bg: #f9f5f1;
    --surface: #ffffff;
    --text: #2d2a26;
    --text-secondary: #7c7670;
    --accent: #c96442;
    --accent-light: #f3e8e2;
    --border: #e8e2dc;
    --chat-user-bg: #f3e8e2;
    --chat-bot-bg: #ffffff;
    --green: #3d8c40;
    --yellow: #b8860b;
    --red: #c44536;
}

/* Full page bg */
.stApp {background: var(--bg) !important; font-family: 'Inter', sans-serif; color: var(--text);}

/* Main container */
.main-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
}
.main-header h1 {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    color: var(--text);
}
.main-header .subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* Chat messages */
.msg-container {
    max-width: 720px;
    margin: 0 auto;
    padding: 1rem 1.5rem;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0;
}
.msg-user .bubble {
    background: var(--chat-user-bg);
    padding: 0.75rem 1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.msg-bot {
    margin: 1rem 0;
}
.msg-bot .bubble {
    background: var(--chat-bot-bg);
    border: 1px solid var(--border);
    padding: 1rem 1.25rem;
    border-radius: 4px 18px 18px 18px;
    max-width: 90%;
    font-size: 0.9rem;
    line-height: 1.65;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.msg-bot .avatar {
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}

/* Recipe card inside chat */
.recipe-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.75rem 0;
}
.recipe-card .name {
    font-family: 'Source Serif 4', serif;
    font-size: 1.1rem;
    font-weight: 600;
}
.recipe-card .meta {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.2rem;
}
.recipe-card .score-bar {
    display: inline-block;
    background: var(--accent-light);
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent);
    margin-top: 0.4rem;
}
.recipe-card .reasons {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    line-height: 1.6;
}

/* Quick prompt pills */
.pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    padding: 0.75rem 0;
}
.pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.4rem 1rem;
    font-size: 0.82rem;
    color: var(--text);
    cursor: pointer;
    transition: all 0.15s;
    text-decoration: none;
}
.pill:hover {background: var(--accent-light); border-color: var(--accent);}

/* Nutrition mini bars */
.nutr-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.3rem 0;
    font-size: 0.8rem;
}
.nutr-label {width: 65px; color: var(--text-secondary);}
.nutr-bar {flex: 1; background: #ede8e3; border-radius: 4px; height: 6px; overflow: hidden;}
.nutr-fill {height: 100%; border-radius: 4px; transition: width 0.4s;}
.nutr-pct {width: 35px; text-align: right; font-weight: 500; font-size: 0.75rem;}

/* Context panel */
.ctx-panel {
    background: var(--surface);
    border-left: 1px solid var(--border);
    padding: 1.25rem;
    height: 100vh;
    overflow-y: auto;
    position: sticky;
    top: 0;
}
.ctx-section {margin-bottom: 1.5rem;}
.ctx-section h3 {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    font-weight: 600;
}

/* Input area */
div[data-testid="stChatInput"] {
    max-width: 720px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───
if "messages" not in st.session_state:
    st.session_state.messages = []
if "recs" not in st.session_state:
    st.session_state.recs = None
if "ics_url" not in st.session_state:
    st.session_state.ics_url = ""

# ─── Load Data ───
@st.cache_data
def load():
    return recipe_data.load_recipes(), recipe_data.load_pantry(), recipe_data.load_nutrition_goals()

all_recipes, pantry, goals = load()


# ══════════════════════════════════════════════
# RESPONSE GENERATORS (must be before UI code)
# ══════════════════════════════════════════════

def _recommend_response(free_mins, text, skip_first=False):
    boost = None
    max_time = free_mins
    if "protein" in text:
        boost = "protein"
    elif "quick" in text or "fast" in text or "30" in text:
        boost = "quick"
        max_time = min(max_time, 30)
    elif "comfort" in text or "favorite" in text:
        boost = "comfort"
    elif "pantry" in text or "what i have" in text:
        boost = "pantry"

    results = scorer.score_recipes(all_recipes, max_time, pantry, goals, boost)
    if skip_first and len(results) > 1:
        results = results[1:]
    if not results:
        return f"Nothing fits a {max_time}-minute window right now. Try asking for more time?"

    st.session_state.recs = results
    cards_html = ""
    for i, res in enumerate(results[:3]):
        rec = res["recipe"]
        reasons_html = "<br>".join(res["reasons"])
        medal = ["🥇", "🥈", "🥉"][i]
        cards_html += f'''<div class="recipe-card">
            <div class="name">{medal} {rec["name"]}</div>
            <div class="meta">{rec["cuisine"]} · {rec["difficulty"]} · {rec["total_minutes"]} min · ⭐ {rec["family_rating"]}/5</div>
            <div class="score-bar">Match: {res["score"]}%</div>
            <div class="reasons">{reasons_html}</div>
            <div class="meta" style="margin-top:0.5rem">P:{rec["protein_g"]}g · Fiber:{rec["fiber_g"]}g · {rec["calories"]}cal</div>
        </div>'''

    weekly = scorer.get_weekly_nutrition()
    p_pct = round(weekly["protein"] / goals["protein"] * 100) if goals["protein"] else 0
    cal_note = f"You have **{max_time} minutes** free tonight." if max_time < 240 else "Evening looks clear."
    gap_note = f" Protein is at **{p_pct}%** for the week, so I'm prioritizing that." if p_pct < 50 else ""
    return f'''{cal_note}{gap_note}

Here's what I'd suggest:

{cards_html}

Say **"I'll cook [name]"** to log it, or **"suggest another"** for more options.'''


def _nutrition_response():
    weekly = scorer.get_weekly_nutrition()
    log = scorer.load_meal_log()
    week_start = date.today() - timedelta(days=date.today().weekday())
    meals = [e for e in log if date.fromisoformat(e["date"]) >= week_start]
    p_pct = round(weekly["protein"] / goals["protein"] * 100)
    f_pct = round(weekly["fiber"] / goals["fiber"] * 100)
    c_pct = round(weekly["calories"] / goals["calories"] * 100)
    meal_list = ""
    for m in meals[-5:]:
        meal_list += f"<br>• {m['date']} — {m['recipe']} (P:{m['protein_g']}g, Fiber:{m['fiber_g']}g)"
    tip = "⚠️ Protein needs a boost — try Palak Paneer, Paneer Butter Masala, or Rajma tonight." if p_pct < 40 else "✅ Looking good!"
    return f'''Here's your week so far ({len(meals)} meals logged):

**💪 Protein:** {weekly["protein"]}g / {goals["protein"]}g ({p_pct}%)
**🥬 Fiber:** {weekly["fiber"]}g / {goals["fiber"]}g ({f_pct}%)
**🔥 Calories:** {weekly["calories"]} / {goals["calories"]} ({c_pct}%)

Recent meals:{meal_list}

{tip}'''


def _pantry_response():
    in_stock = sorted([k for k, v in pantry.items() if v])
    to_buy = sorted([k for k, v in pantry.items() if not v])
    return f'''**In stock ({len(in_stock)} items):**
{", ".join(in_stock)}

**Need to buy ({len(to_buy)}):**
{", ".join(to_buy)}'''


def _log_response(text):
    matched = None
    for recipe in all_recipes:
        if recipe["name"].lower() in text:
            matched = recipe
            break
    if not matched and st.session_state.recs:
        matched = st.session_state.recs[0]["recipe"]
    if matched:
        scorer.log_meal(matched["name"], matched["protein_g"], matched["fiber_g"], matched["calories"])
        st.cache_data.clear()
        weekly = scorer.get_weekly_nutrition()
        p_pct = round(weekly["protein"] / goals["protein"] * 100)
        return f'''✅ **Logged: {matched["name"]}**

Added {matched["protein_g"]}g protein, {matched["fiber_g"]}g fiber, {matched["calories"]} cal.
Protein is now at **{p_pct}%** for the week. Enjoy! 🎉'''
    else:
        return 'Which recipe? Say **"I cooked Palak Paneer"** or **"log Dal Tadka"**.'


# ─── Layout: Chat (left) | Context Panel (right) ───
chat_col, ctx_col = st.columns([3, 1.2], gap="small")

# ══════════════════════════════════════════════
# RIGHT: CONTEXT PANEL
# ══════════════════════════════════════════════
with ctx_col:
    st.markdown('<div class="ctx-panel">', unsafe_allow_html=True)
    
    # Calendar
    st.markdown('<div class="ctx-section"><h3>📅 Calendar</h3></div>', unsafe_allow_html=True)
    ics_url = st.text_input(
        "ICS link", value=st.session_state.ics_url,
        placeholder="Paste your Outlook ICS link...",
        label_visibility="collapsed",
        help="Settings → Calendar → Shared calendars → Publish → Copy ICS link"
    )
    st.session_state.ics_url = ics_url
    
    free_minutes, cal_summary = cal_ics.get_cooking_window(ics_url if ics_url else None)
    
    if ics_url:
        st.caption(f"🟢 {cal_summary}")
    else:
        free_minutes = st.slider("Free time tonight (min)", 15, 240, 90, 15)
        st.caption("Connect calendar for real data")
    
    # Nutrition
    st.markdown('<div class="ctx-section"><h3>💪 This Week</h3></div>', unsafe_allow_html=True)
    weekly = scorer.get_weekly_nutrition()
    
    for macro, target, icon in [("protein", goals["protein"], "💪"), ("fiber", goals["fiber"], "🥬"), ("calories", goals["calories"], "🔥")]:
        consumed = weekly[macro]
        pct = round(consumed / target * 100) if target else 0
        color = "var(--green)" if pct >= 60 else "var(--yellow)" if pct >= 30 else "var(--red)"
        unit = "kcal" if macro == "calories" else "g"
        st.markdown(f"""
        <div class="nutr-row">
            <span class="nutr-label">{icon} {macro.title()}</span>
            <div class="nutr-bar"><div class="nutr-fill" style="width:{min(pct,100)}%;background:{color}"></div></div>
            <span class="nutr-pct">{pct}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    meals = len([e for e in scorer.load_meal_log() if date.fromisoformat(e["date"]) >= date.today() - timedelta(days=date.today().weekday())])
    st.caption(f"{meals} meals logged · {weekly['protein']}g protein · {weekly['fiber']}g fiber")
    
    # Recipe count
    st.markdown('<div class="ctx-section"><h3>📖 Recipes</h3></div>', unsafe_allow_html=True)
    cuisines = {}
    for r in all_recipes:
        cuisines[r["cuisine"]] = cuisines.get(r["cuisine"], 0) + 1
    for cuisine, count in sorted(cuisines.items(), key=lambda x: -x[1]):
        st.caption(f"{cuisine}: {count}")
    
    # Pantry
    st.markdown('<div class="ctx-section"><h3>🥫 Pantry</h3></div>', unsafe_allow_html=True)
    in_stock = sum(1 for v in pantry.values() if v)
    st.caption(f"{in_stock} items in stock")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# LEFT: CHAT
# ══════════════════════════════════════════════
with chat_col:
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🍳 RecipeBot</h1>
        <div class="subtitle">What should we cook tonight?</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Empty state: show quick prompts
    if not st.session_state.messages:
        st.markdown('<div class="msg-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding: 3rem 1rem 1rem; color: var(--text-secondary); font-size: 0.9rem;">
            Ask me what to cook — I'll check your calendar, nutrition gaps, pantry, and family favorites.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            if st.button("🍳 What to cook?", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "What should I cook tonight?"})
                st.rerun()
        with p2:
            if st.button("⚡ Something quick", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "Something quick, under 30 minutes"})
                st.rerun()
        with p3:
            if st.button("💪 High protein", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "I need something high in protein"})
                st.rerun()
        with p4:
            if st.button("🌮 Something new", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "Suggest something different we haven't had recently"})
                st.rerun()
    
    # Render chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-container"><div class="msg-user">
                <div class="bubble">{msg["text"]}</div>
            </div></div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-container"><div class="msg-bot">
                <div class="avatar">🍳</div>
                <div class="bubble">{msg["text"]}</div>
            </div></div>
            """, unsafe_allow_html=True)
    
    # Process last user message
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last = st.session_state.messages[-1]["text"].lower()
        
        # ─── Determine intent ───
        if any(w in last for w in ["nutrition", "macro", "progress", "goal", "how am i"]):
            response = _nutrition_response()
        elif any(w in last for w in ["pantry", "ingredients", "what do i have"]):
            response = _pantry_response()
        elif any(w in last for w in ["log", "cooked", "i made", "i'll cook"]):
            response = _log_response(last)
        elif any(w in last for w in ["another", "skip", "different", "next"]):
            response = _recommend_response(free_minutes, last, skip_first=True)
        else:
            response = _recommend_response(free_minutes, last)
        
        st.session_state.messages.append({"role": "bot", "text": response})
        st.rerun()
    
    # Chat input
    user_input = st.chat_input("What should we cook tonight?")
    if user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        st.rerun()
