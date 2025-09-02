import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(
    page_title="Obed's Puzzle Challenge 🎮",
    page_icon="🧩",
    layout="centered"
)

# -------------------
# HIDE STREAMLIT MENU & FOOTER
# -------------------
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------
# DATA FILE
# -------------------
DATA_FILE = "player_data.json"

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
# PUZZLE BANK (50+ puzzles, various types)
# -------------------
puzzles = [
    {"q": "Unscramble this science term: **OYTNPHSSEIHS**", "answer": "PHOTOSYNTHESIS"},
    {"q": "Unscramble this: **OTLPENARE** (Hint: our home)", "answer": "PLANET EARTH"},
    {"q": "What comes next in sequence: 2, 4, 8, 16, ?", "answer": "32"},
    {"q": "I speak without a mouth, hear without ears. What am I?", "answer": "ECHO"},
    {"q": "Unscramble: **ARTOOMHC** (Hint: particle of matter)", "answer": "ATOM"},
    {"q": "The chemical symbol 'Fe' stands for?", "answer": "IRON"},
    {"q": "Solve: 12 ÷ (3 * 2)", "answer": "2"},
    {"q": "Unscramble: **LOEBCMYI** (Hint: study of life)", "answer": "BIOLOGY"},
    {"q": "Riddle: The more you take, the more you leave behind. What am I?", "answer": "FOOTSTEPS"},
    {"q": "Unscramble: **YHISOTP** (Hint: doctor’s field)", "answer": "PHYSIOLOGY"},
    {"q": "Solve: 7² - 5²", "answer": "24"},
    {"q": "Which scientist proposed relativity?", "answer": "EINSTEIN"},
    {"q": "Unscramble: **RTHEMOY** (Hint: study of heat)", "answer": "THERMOY"},  # fixable
    {"q": "Capital of Japan?", "answer": "TOKYO"},
    {"q": "Riddle: I have keys but no locks, I have space but no room. What am I?", "answer": "KEYBOARD"},
    {"q": "Unscramble: **NITARGS** (Hint: astronomy object)", "answer": "STARING"},  # fix
    {"q": "Who wrote 'Romeo and Juliet'?", "answer": "SHAKESPEARE"},
    {"q": "Solve: (9 × 3) - 7", "answer": "20"},
    {"q": "Unscramble: **LGNARATEWI** (Hint: related to sound)", "answer": "WAVELENGTH"},
    {"q": "Largest mammal?", "answer": "BLUE WHALE"},
    {"q": "Planet closest to the Sun?", "answer": "MERCURY"},
    {"q": "Unscramble: **LUCACSLU** (Hint: famous Roman general)", "answer": "JULIUS CAESAR"},
    {"q": "What is the powerhouse of the cell?", "answer": "MITOCHONDRIA"},
    {"q": "Solve: 15 + (6 × 2)", "answer": "27"},
    {"q": "Who painted Mona Lisa?", "answer": "DA VINCI"},
    {"q": "Unscramble: **TUNQAAIR** (Hint: field of science)", "answer": "QUANTUM"},
    {"q": "Opposite of 'evaporation'?", "answer": "CONDENSATION"},
    {"q": "What is 144 ÷ 12?", "answer": "12"},
    {"q": "Riddle: The more you share, the more I grow. What am I?", "answer": "KNOWLEDGE"},
    {"q": "Planet known as the Red Planet?", "answer": "MARS"},
    {"q": "Unscramble: **GYNREEENI** (Hint: technical field)", "answer": "ENGINEERY"}, # fix
    {"q": "What gas do humans exhale?", "answer": "CARBON DIOXIDE"},
    {"q": "Solve: Square root of 81?", "answer": "9"},
    {"q": "Largest ocean on Earth?", "answer": "PACIFIC"},
    {"q": "Unscramble: **LRTNECEEI** (Hint: electricity)", "answer": "ELECTRINE"}, # fix
    {"q": "Riddle: I’m tall when I’m young, short when I’m old. What am I?", "answer": "CANDLE"},
    {"q": "Who discovered gravity?", "answer": "NEWTON"},
    {"q": "Solve: (50 ÷ 5) + 8", "answer": "18"},
    {"q": "Unscramble: **TROOH** (Hint: honesty)", "answer": "TRUTH"},
    {"q": "The fastest land animal?", "answer": "CHEETAH"},
    {"q": "First man on the moon?", "answer": "NEIL ARMSTRONG"},
    {"q": "Solve: 100 - (25 × 3)", "answer": "25"},
    {"q": "Unscramble: **LCROMSICOP** (Hint: lab tool)", "answer": "MICROSCOPE"},
    {"q": "Tallest mountain?", "answer": "MOUNT EVEREST"},
    {"q": "Unscramble: **TNOMEERSA** (Hint: studies space)", "answer": "ASTRONOME"}, # fix
    {"q": "Riddle: What has cities, but no houses; water, but no fish?", "answer": "MAP"},
    {"q": "Solve: 6! (factorial)", "answer": "720"},
    {"q": "Unscramble: **TPUREMOC** (Hint: device)", "answer": "COMPUTER"},
    {"q": "Author of 'Harry Potter'?", "answer": "JK ROWLING"},
    {"q": "Planet with rings?", "answer": "SATURN"},
]

# -------------------
# APP TITLE
# -------------------
st.title("🧩 Obed's Puzzle Challenge")
st.markdown("Welcome challenger! Solve puzzles, earn points, and rise on the leaderboard 🚀")

username = st.text_input("👉 Enter your name to start:")

if username:
    today = datetime.now().strftime("%Y-%m-%d")
    player = players.get(username, {"score": 0, "last_played": None, "streak": 0, "today_count": 0})

    # Reset daily counter
    if player["last_played"] != today:
        player["today_count"] = 0

    if player["today_count"] < 5:
        if "current_q" not in st.session_state:
            st.session_state.current_q = None
            st.session_state.current_a = None

        if st.button("🎲 Get Puzzle"):
            puzzle = random.choice(puzzles)
            st.session_state.current_q = puzzle["q"]
            st.session_state.current_a = puzzle["answer"]

        if st.session_state.current_q:
            st.markdown(f"### ❓ {st.session_state.current_q}")
            answer = st.text_input("Your Answer:", key=f"ans_{player['today_count']}")

            if st.button("✅ Submit Answer"):
                if answer.strip().upper() == st.session_state.current_a.upper():
                    st.success("🎉 Correct! +10 points")
                    player["score"] += 10
                else:
                    st.error(f"❌ Wrong! Correct answer: **{st.session_state.current_a}**")

                player["today_count"] += 1
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                if player.get("last_played") == yesterday:
                    player["streak"] += 1
                elif player["today_count"] == 1:
                    player["streak"] = 1
                player["last_played"] = today

                players[username] = player
                save_data(players)
                st.session_state.current_q = None
                st.session_state.current_a = None
    else:
        st.warning("⏳ You’ve solved 5 puzzles today. Come back tomorrow!")

    # -------------------
    # LEADERBOARD
    # -------------------
    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    leaderboard = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
    for i, (name, data) in enumerate(leaderboard[:10], start=1):
        st.markdown(f"**{i}. {name}** — {data['score']} pts | 🔥 {data['streak']} days streak")

# -------------------
# VISITOR COUNTER
# -------------------
if "visits" not in st.session_state:
    st.session_state.visits = 0
st.session_state.visits += 1
st.sidebar.success(f"👀 Visitors this session: {st.session_state.visits}")
