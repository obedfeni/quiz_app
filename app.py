import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

# -------------------
# CONFIG
# -------------------
st.set_page_config(
    page_title="Answer Obed's Questions 🎮",
    page_icon="🎯",
    layout="centered"
)

DATA_FILE = "player_data.json"
PLAYS_PER_DAY = 3
POINTS_PER_CORRECT = 10

# -------------------
# LOAD / SAVE DATA
# -------------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # default structure
    return {"players": {}, "visitors": 0}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

data = load_data()
players = data.get("players", {})
visitors = data.get("visitors", 0)

# -------------------
# PUZZLE WORDS (50) — used for "Puzzle Words" category
# -------------------
puzzles = [
    {"word": "ELEPHANT", "hint": "The largest land animal"},
    {"word": "BANANA", "hint": "Yellow fruit loved by monkeys"},
    {"word": "GUITAR", "hint": "A six-stringed musical instrument"},
    {"word": "PYRAMID", "hint": "Famous triangular structures in Egypt"},
    {"word": "OXYGEN", "hint": "Gas essential for breathing"},
    {"word": "VOLCANO", "hint": "Mountain that erupts lava"},
    {"word": "JUPITER", "hint": "Largest planet in our solar system"},
    {"word": "CLOCK", "hint": "Tells the time"},
    {"word": "UMBRELLA", "hint": "Used on a rainy day"},
    {"word": "BICYCLE", "hint": "Two-wheeled vehicle you pedal"},
    {"word": "BRIDGE", "hint": "Structure that connects two places"},
    {"word": "RAINBOW", "hint": "Colorful arc seen after rain"},
    {"word": "CANDLE", "hint": "Wax stick with a flame"},
    {"word": "PRISON", "hint": "Where criminals are kept"},
    {"word": "COMPUTER", "hint": "Machine for processing data"},
    {"word": "EAGLE", "hint": "Bird with sharp vision"},
    {"word": "DRAGON", "hint": "Mythical fire-breathing creature"},
    {"word": "ISLAND", "hint": "Land surrounded by water"},
    {"word": "SCHOOL", "hint": "Place where students learn"},
    {"word": "LADDER", "hint": "Used to climb up and down"},
    {"word": "PLANET", "hint": "Orbits a star like the sun"},
    {"word": "ZEBRA", "hint": "Striped African animal"},
    {"word": "HONEY", "hint": "Made by bees"},
    {"word": "MIRROR", "hint": "Reflects your image"},
    {"word": "RIVER", "hint": "Flows to the sea"},
    {"word": "MARKET", "hint": "Place to buy and sell goods"},
    {"word": "TIGER", "hint": "Striped big cat"},
    {"word": "CHAIR", "hint": "Furniture for sitting"},
    {"word": "SPIDER", "hint": "Eight-legged web spinner"},
    {"word": "PENCIL", "hint": "Used for writing or drawing"},
    {"word": "CASTLE", "hint": "Fortress for kings and queens"},
    {"word": "FIREWORK", "hint": "Explodes in colorful lights"},
    {"word": "CAMERA", "hint": "Used to take photos"},
    {"word": "BOTTLE", "hint": "Holds water or drinks"},
    {"word": "TRAIN", "hint": "Moves on tracks"},
    {"word": "MOUNTAIN", "hint": "Tall natural elevation"},
    {"word": "WINDOW", "hint": "Transparent part of a wall"},
    {"word": "BASKET", "hint": "Woven container"},
    {"word": "ROBOT", "hint": "Machine that can move and act"},
    {"word": "OCEAN", "hint": "Covers most of Earth"},
    {"word": "CLOUD", "hint": "White and fluffy in the sky"},
    {"word": "DOCTOR", "hint": "Heals sick people"},
    {"word": "PIZZA", "hint": "Italian food with cheese"},
    {"word": "CROWN", "hint": "Worn by kings and queens"},
    {"word": "TELEPHONE", "hint": "Used to make calls"},
    {"word": "BALL", "hint": "Round object used in games"},
    {"word": "MARKER", "hint": "Used for coloring or writing"},
    {"word": "PILOT", "hint": "Flies an airplane"},
    {"word": "TORCH", "hint": "Portable light source"},
]
PUZZLE_WORDS = [p["word"] for p in puzzles]

def build_puzzle_options(answer: str, k: int = 3):
    """Pick plausible distractors:
       - Prefer same first letter and similar length (±1)
       - Fallback to same length, then any word
    """
    ans = answer.upper()
    candidates = [w for w in PUZZLE_WORDS if w != ans]
    same_first = [w for w in candidates if w[0] == ans[0]]
    similar_len = [w for w in candidates if abs(len(w) - len(ans)) <= 1]

    pool = [w for w in same_first if abs(len(w) - len(ans)) <= 1]
    if len(pool) < k:
        pool = list(set(similar_len) - {ans})  # unique
    if len(pool) < k:
        pool = candidates

    distractors = random.sample(pool, k) if len(pool) >= k else random.sample(candidates, min(k, len(candidates)))
    options = distractors + [ans]
    random.shuffle(options)
    return options

# -------------------
# QUESTION BANK (MULTIPLE CHOICE)
# -------------------
questions = {
    "About Obed": [
        {"q": "favorite sports?", "options": ["football", "", "basketball", "table tennis"], "answer": "football"},
        {"q": "guess my age?", "options": ["22", "24", "26", "28"], "answer": "24"},
        {"q": "guess my height?", "options": ["5'8", "5'2", "6'4", "6'1"], "answer": "5'8"},
        {"q": "What is Obed’s favorite movie?", "options": ["Inception", "Black Panther", "Titanic", "Avengers"], "answer": "Black Panther"},
    ],
    "Science": [
        {"q": "What is H2O commonly known as?", "options": ["Water", "Oxygen", "Hydrogen", "Salt"], "answer": "Water"},
        {"q": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars"},
        {"q": "Who invented the light bulb?", "options": ["Edison", "Newton", "Tesla", "Einstein"], "answer": "Edison"},
        {"q": "The speed of light is approximately…", "options": ["3,000 km/s", "30,000 km/s", "300,000 km/s", "3,000,000 km/s"], "answer": "300,000 km/s"},
    ],
    "History & Arts": [
        {"q": "Who painted the Mona Lisa?", "options": ["Picasso", "Da Vinci", "Van Gogh", "Rembrandt"], "answer": "Da Vinci"},
        {"q": "The Great Pyramid of Giza is in which country?", "options": ["Egypt", "Sudan", "Mexico", "India"], "answer": "Egypt"},
        {"q": "Which empire built the Colosseum?", "options": ["Greek", "Roman", "Ottoman", "Byzantine"], "answer": "Roman"},
    ],
    # For "Puzzle Words" we will generate options dynamically for each picked word
}

# -------------------
# UI HEADER
# -------------------
st.markdown(
    """
    <div style="text-align:center; padding: 8px 0 14px;">
      <h1 style="margin-bottom:4px">🎯 Answer Obed's Questions</h1>
      <p style="margin-top:0; font-size:1.05rem;">Play daily, earn points, keep your streak, and climb the leaderboard 🚀</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------
# USERNAME / VISITOR COUNT
# -------------------
username = st.text_input("👤 Enter your name to start:")

if not username:
    st.info("Tip: Use the same name every time so your points and streak are saved.")
    st.stop()

# New visitor? count & create baseline record immediately
if username not in players:
    visitors += 1
    players[username] = {"score": 0, "last_played": None, "streak": 0, "today_count": 0, "categories": {}}
    data["players"] = players
    data["visitors"] = visitors
    save_data(data)

player = players[username]
today_str = datetime.now().strftime("%Y-%m-%d")
if player["last_played"] != today_str:
    player["today_count"] = 0  # reset daily plays

# -------------------
# SESSION STATE (freeze question + options)
# -------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = None  # dict: {"q", "answer", "category"}
if "current_options" not in st.session_state:
    st.session_state.current_options = None  # list[str]
if "q_session_id" not in st.session_state:
    st.session_state.q_session_id = 0  # increments to reset widgets

# -------------------
# DAILY INFO
# -------------------
remaining = max(0, PLAYS_PER_DAY - player["today_count"])
st.markdown(f"**🗓️ Daily plays left:** {remaining} / {PLAYS_PER_DAY}")

# -------------------
# GAME AREA
# -------------------
if remaining == 0:
    st.warning("⏳ You’ve reached your daily limit. Come back tomorrow!")
else:
    st.subheader("📂 Choose a category:")
    category_names = list(questions.keys()) + ["Puzzle Words"]
    category = st.selectbox("Categories", category_names)

    colA, colB = st.columns(2)
    with colA:
        if st.button("🎲 Get a Question"):
            # pick and freeze a new question
            if category == "Puzzle Words":
                picked = random.choice(puzzles)
                q_text = f"Which word fits this hint?\n\n💡 {picked['hint']}"
                answer = picked["word"].upper()
                options = build_puzzle_options(answer, k=3)
            else:
                q_obj = random.choice(questions[category])
                q_text = q_obj["q"]
                answer = q_obj["answer"]
                options = q_obj["options"][:]  # copy
                random.shuffle(options)

            st.session_state.current_q = {"q": q_text, "answer": answer, "category": category}
            st.session_state.current_options = options
            st.session_state.q_session_id += 1  # force fresh radio widget

    # show frozen question
    if st.session_state.current_q:
        q = st.session_state.current_q
        opts = st.session_state.current_options or []

        st.markdown(f"### ❓ {q['q']}")
        choice = st.radio(
            "Pick one:",
            opts,
            key=f"choice_{st.session_state.q_session_id}"
        )

        if st.button("✅ Submit Answer"):
            # capture previous before update (for streak)
            previously_played = player["last_played"]
            yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            if choice == q["answer"]:
                st.success(f"🎉 Correct! +{POINTS_PER_CORRECT} points")
                player["score"] += POINTS_PER_CORRECT
                # per-category points
                cat = q["category"]
                player["categories"][cat] = player["categories"].get(cat, 0) + POINTS_PER_CORRECT
            else:
                st.error(f"❌ Wrong! The correct answer is **{q['answer']}**.")

            # update plays & streak
            player["today_count"] += 1
            player["last_played"] = today_str
            if previously_played == yesterday_str:
                player["streak"] += 1
            elif player["today_count"] == 1:
                player["streak"] = 1

            # persist
            players[username] = player
            data["players"] = players
            save_data(data)

            # clear frozen question
            st.session_state.current_q = None
            st.session_state.current_options = None

            # if limit reached show share box immediately
            if player["today_count"] >= PLAYS_PER_DAY:
                st.warning("⏳ That was your last play for today. Come back tomorrow!")
                share_text = (
                    f"🎯 I just played *Answer Obed's Questions!* \n"
                    f"🏆 Score: {player['score']} pts | 🔥 Streak: {player['streak']} days\n"
                    f"📅 {today_str}\n"
                    f"Play here 👉 https://answermufasaquestions.streamlit.app/"
                )
                st.text_area("📤 Copy & share your results:", share_text, height=120)

# -------------------
# LEADERBOARD (Global)
# -------------------
st.markdown("---")
st.subheader("🏆 Leaderboard")
if players:
    leaderboard = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
    for i, (name, pdata) in enumerate(leaderboard[:10], start=1):
        st.markdown(
            f"<div style='padding:8px;border-radius:10px;background:#f7f7f7;margin:6px 0;'>"
            f"<b>{i}. {name}</b> — {pdata['score']} pts &nbsp;|&nbsp; 🔥 {pdata.get('streak',0)} days"
            f"</div>", unsafe_allow_html=True
        )
else:
    st.caption("No players yet. Be the first to play!")

# -------------------
# FOOTER
# -------------------
st.markdown("---")
st.info(f"👀 Total visitors so far: **{visitors}**")
