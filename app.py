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

# -------------------
# LOAD / SAVE DATA
# -------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"players": {}, "visitors": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()
players = data.get("players", {})
visitors = data.get("visitors", 0)

# -------------------
# PUZZLE BANK (50 words)
# -------------------
puzzles = [
    {"word": "PYTHON", "hint": "A popular programming language"},
    {"word": "CAMERA", "hint": "Used for photography"},
    {"word": "STREAMLIT", "hint": "Framework we are using"},
    {"word": "AFRICA", "hint": "Obed’s home continent"},
    {"word": "PLANET", "hint": "Orbits around a star"},
    {"word": "RIVER", "hint": "Flows into oceans or lakes"},
    {"word": "MUSIC", "hint": "Universal language of sound"},
    {"word": "OCEAN", "hint": "Covers most of Earth"},
    {"word": "CLOUD", "hint": "Floats in the sky"},
    {"word": "TREE", "hint": "Has leaves and gives shade"},
    {"word": "BOOK", "hint": "Made of pages and words"},
    {"word": "LIGHT", "hint": "Opposite of darkness"},
    {"word": "FIRE", "hint": "Provides heat, can burn"},
    {"word": "WATER", "hint": "Essential for life"},
    {"word": "BRAIN", "hint": "Controls the body"},
    {"word": "HEART", "hint": "Pumps blood"},
    {"word": "PHONE", "hint": "Used to call people"},
    {"word": "TRAIN", "hint": "Runs on tracks"},
    {"word": "CAR", "hint": "Has four wheels"},
    {"word": "HOUSE", "hint": "Where people live"},
    {"word": "SUN", "hint": "Star at the center of solar system"},
    {"word": "MOON", "hint": "Earth’s natural satellite"},
    {"word": "STAR", "hint": "Shines in the night sky"},
    {"word": "ROAD", "hint": "Where cars drive"},
    {"word": "SHIP", "hint": "Travels on water"},
    {"word": "CLOCK", "hint": "Tells time"},
    {"word": "MAP", "hint": "Shows directions"},
    {"word": "KEY", "hint": "Opens locks"},
    {"word": "CHAIR", "hint": "You sit on it"},
    {"word": "TABLE", "hint": "You eat on it"},
    {"word": "PEN", "hint": "Used for writing"},
    {"word": "PAPER", "hint": "You write on it"},
    {"word": "LION", "hint": "King of the jungle"},
    {"word": "DOG", "hint": "Man’s best friend"},
    {"word": "CAT", "hint": "Likes to chase mice"},
    {"word": "HORSE", "hint": "Fast running animal"},
    {"word": "BIRD", "hint": "Has wings"},
    {"word": "FISH", "hint": "Lives in water"},
    {"word": "EGG", "hint": "Laid by chickens"},
    {"word": "MILK", "hint": "Comes from cows"},
    {"word": "CHEESE", "hint": "Made from milk"},
    {"word": "BREAD", "hint": "Staple food"},
    {"word": "APPLE", "hint": "Keeps the doctor away"},
    {"word": "ORANGE", "hint": "Citrus fruit"},
    {"word": "BANANA", "hint": "Long yellow fruit"},
    {"word": "MANGO", "hint": "Sweet tropical fruit"},
    {"word": "GRAPE", "hint": "Can be made into wine"},
    {"word": "PEAR", "hint": "Shaped like a bell"},
    {"word": "PEACH", "hint": "Fuzzy fruit"},
]

# -------------------
# QUESTION BANK
# -------------------
questions = {
    "About Obed": [
        {"q": "What is Obed Feni’s African house name?", "options": ["Kobby", "Kojo", "Nana", "Kwame"], "answer": "Kobby"},
        {"q": "How old is Obed Feni?", "options": ["22", "24", "26", "28"], "answer": "24"},
        {"q": "What is Obed’s favorite food?", "options": ["Jollof Rice", "Pizza", "Fufu", "Banku"], "answer": "Jollof Rice"},
        {"q": "What is Obed’s favorite movie?", "options": ["Inception", "Black Panther", "Titanic", "Avengers"], "answer": "Black Panther"},
    ],
    "Science & STEM": [
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
    "Puzzle Words": [
        {"q": p["hint"], "options": random.sample([w["word"] for w in puzzles if w != p], 3) + [p["word"]], "answer": p["word"]}
        for p in puzzles
    ],
}

# -------------------
# MAIN APP
# -------------------
st.title("🎯 Answer Obed's Questions!")
st.markdown("Welcome! Play daily, earn points, and climb the leaderboard 🚀")

username = st.text_input("👉 Enter your name to start:")

if username:
    today = datetime.now().strftime("%Y-%m-%d")

    # New visitor? Count them
    if username not in players:
        visitors += 1
        data["visitors"] = visitors

    player = players.get(username, {"score": 0, "last_played": None, "streak": 0, "today_count": 0})

    # Reset daily counter
    if player["last_played"] != today:
        player["today_count"] = 0

    # -------------------
    # GAME LOGIC
    # -------------------
    if player["today_count"] < 3:
        st.subheader("📂 Choose a category:")
        category = st.selectbox("Categories", list(questions.keys()))

        if "current_q" not in st.session_state:
            st.session_state.current_q = None

        if st.button("🎲 Get a Question"):
            st.session_state.current_q = random.choice(questions[category])

        if st.session_state.current_q:
            q = st.session_state.current_q
            st.markdown(f"### ❓ {q['q']}")
            options = q["options"].copy()
            random.shuffle(options)
            choice = st.radio("Pick one:", options, key=f"choice_{player['today_count']}")

            if st.button("✅ Submit Answer"):
                if q["answer"] and choice == q["answer"]:
                    st.success("🎉 Correct! +10 points")
                    player["score"] += 10
                else:
                    st.error(f"❌ Wrong! The correct answer is **{q['answer']}**.")

                player["today_count"] += 1
                player["last_played"] = today

                # Streak logic
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                if player.get("last_played") == yesterday:
                    player["streak"] += 1
                elif player["today_count"] == 1:
                    player["streak"] = 1

                players[username] = player
                data["players"] = players
                save_data(data)

                # Clear question
                st.session_state.current_q = None

    else:
        st.warning("⏳ You’ve answered 3 questions today. Come back tomorrow!")

        # Shareable results
        share_text = f"""
📢 I just played *Answer Obed's Questions!* 🎯
🏆 Score: {player['score']} pts
🔥 Streak: {player['streak']} days
📅 Date: {today}

Play here 👉 https://answermufasaquestions.streamlit.app/
        """
        st.text_area("📤 Copy & share your results:", share_text, height=120)

    # -------------------
    # LEADERBOARD
    # -------------------
    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    leaderboard = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)

    for i, (name, pdata) in enumerate(leaderboard[:10], start=1):
        st.markdown(
            f"**{i}. {name}** — {pdata['score']} pts | 🔥 Streak: {pdata['streak']} days"
        )

    # -------------------
    # FOOTER
    # -------------------
    st.markdown("---")
    st.info(f"👀 Total visitors so far: **{visitors}**")
