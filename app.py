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
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

players = load_data()

# -------------------
# QUESTION BANK
# -------------------
questions = {
    "About Obed": [
        {"q": "What is Obed Feni’s African house name?", "options": ["Kobby", "Kojo", "Nana", "Kwame"], "answer": "Kobby"},
        {"q": "How old is Obed Feni?", "options": ["22", "24", "26", "28"], "answer": "24"},
        {"q": "What is Obed’s favorite food?", "options": ["Jollof Rice", "Pizza", "Fufu", "Banku"], "answer": "Jollof Rice"},  # <-- update to your real answer
        {"q": "What is Obed’s favorite movie?", "options": ["Inception", "Black Panther", "Titanic", "Avengers"], "answer": "Black Panther"},  # <-- update
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
    "Psychometric & Fun": [
        {"q": "Do you prefer mornings or nights?", "options": ["Mornings", "Nights"], "answer": None},
        {"q": "If you were an animal, which one are you most like?", "options": ["Lion", "Turtle", "Bird", "Monkey"], "answer": None},
        {"q": "You’re given $1,000 — do you spend or save?", "options": ["Spend", "Save"], "answer": None},
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
            choice = st.radio("Pick one:", q["options"], key=f"choice_{player['today_count']}")

            if st.button("✅ Submit Answer"):
                if q["answer"] and choice == q["answer"]:
                    st.success("🎉 Correct! +10 points")
                    player["score"] += 10
                elif q["answer"]:
                    st.error(f"❌ Wrong! The correct answer is **{q['answer']}**.")
                else:
                    st.info(f"✨ Interesting choice: **{choice}**")

                player["today_count"] += 1
                player["last_played"] = today

                # Streak logic
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                if player.get("last_played") == yesterday:
                    player["streak"] += 1
                elif player["today_count"] == 1:
                    player["streak"] = 1

                players[username] = player
                save_data(players)

                # Clear question
                st.session_state.current_q = None

    else:
        st.warning("⏳ You’ve answered 3 questions today. Come back tomorrow!")

    # -------------------
    # LEADERBOARD
    # -------------------
    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    leaderboard = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)

    for i, (name, data) in enumerate(leaderboard[:10], start=1):
        st.markdown(
            f"**{i}. {name}** — {data['score']} pts | 🔥 Streak: {data['streak']} days"
        )
