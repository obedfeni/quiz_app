import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

# -------------------
# CONFIG
# -------------------
st.set_page_config(
    page_title="Obed’s Puzzle Challenge 🧩",
    page_icon="🧠",
    layout="centered"
)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Custom Theme: Blue & White
custom_style = """
    <style>
    body {
        background-color: #f0f6ff; /* Light blue-white background */
        color: #0d1b2a; /* Dark navy text */
    }

    .stApp {
        background-color: #f0f6ff;
    }

    h1, h2, h3, h4 {
        color: #1e3a8a; /* Deep blue headings */
    }

    .stButton>button {
        background-color: #2563eb; /* Bright blue buttons */
        color: white;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1e40af; /* Darker blue on hover */
        color: white;
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #2563eb;
        padding: 0.5em;
    }

    .stAlert {
        border-radius: 10px;
        padding: 1em;
    }

    .css-1d391kg {  /* Leaderboard spacing fix */
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)


DATA_FILE = "player_data.json"

# -------------------
# LOAD / SAVE DATA
# -------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"players": {}, "visits": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()
players = data.get("players", {})
visits = data.get("visits", 0)

# -------------------
# PUZZLE BANK (50+)
# -------------------
puzzles = [
    # Scrambles
    {"q": "Unscramble: **OTPNYH**", "answer": "PYTHON"},
    {"q": "Unscramble: **OCPMUTER**", "answer": "COMPUTER"},
    {"q": "Unscramble: **AHSRC** (used in math)", "answer": "CHAIR"},
    {"q": "Unscramble: **SGNINEERNEI**", "answer": "ENGINEERING"},
    {"q": "Unscramble: **ROTAHPOTOHS** (graphic tool)", "answer": "PHOTOSHOP"},
    {"q": "Unscramble: **ANCMERIA** (country)", "answer": "AMERICA"},
    {"q": "Unscramble: **CTEILEVE** (electric property)", "answer": "VELOCITE"},

    # Logic/Math
    {"q": "What comes next: 1, 1, 2, 3, 5, 8, ?", "answer": "13"},
    {"q": "If a clock strikes 6 in 30 seconds, how long for 12?", "answer": "66"},
    {"q": "Solve: If 5x = 20, what is x?", "answer": "4"},
    {"q": "Which number is missing: 2, 4, 6, ?, 10", "answer": "8"},
    {"q": "What is 12 squared?", "answer": "144"},
    {"q": "I am a two-digit number, sum of digits is 11, difference is 5. What am I?", "answer": "83"},

    # Riddles
    {"q": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
    {"q": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"},
    {"q": "What has hands but cannot clap?", "answer": "clock"},
    {"q": "What can travel around the world while staying in a corner?", "answer": "stamp"},
    {"q": "What has a heart that doesn’t beat?", "answer": "artichoke"},
    {"q": "I’m tall when I’m young, and short when I’m old. What am I?", "answer": "candle"},

    # Science
    {"q": "What is the powerhouse of the cell?", "answer": "mitochondria"},
    {"q": "Water boils at what °C at sea level?", "answer": "100"},
    {"q": "What gas do plants breathe in?", "answer": "carbon dioxide"},
    {"q": "Which planet has the most moons?", "answer": "saturn"},
    {"q": "What is H2O?", "answer": "water"},
    {"q": "Which metal is liquid at room temperature?", "answer": "mercury"},
    {"q": "What does DNA stand for? (short form)", "answer": "dna"},
    
    # History
    {"q": "Who was the first President of the USA?", "answer": "george washington"},
    {"q": "In which year did World War II end?", "answer": "1945"},
    {"q": "The Cold War was mainly USA vs ?", "answer": "ussr"},
    {"q": "Who discovered gravity?", "answer": "isaac newton"},
    {"q": "The pyramids are located in which country?", "answer": "egypt"},
    {"q": "Who was the first man to step on the moon?", "answer": "neil armstrong"},

    # Movies/Books
    {"q": "In Harry Potter, Harry’s owl is named?", "answer": "hedwig"},
    {"q": "Who is the superhero with the shield in Marvel?", "answer": "captain america"},
    {"q": "In The Lion King, Simba’s father is?", "answer": "mufasa"},
    {"q": "Who created Sherlock Holmes?", "answer": "arthur conan doyle"},
    {"q": "In The Matrix, Neo’s real name is?", "answer": "thomas anderson"},
    {"q": "Which movie has the quote: 'May the Force be with you'?", "answer": "star wars"},

    # Daily life
    {"q": "What has keys but can’t open locks?", "answer": "piano"},
    {"q": "Forward I am heavy, backward I am not. What am I?", "answer": "ton"},
    {"q": "What gets wetter as it dries?", "answer": "towel"},
    {"q": "What has one eye but cannot see?", "answer": "needle"},
    {"q": "What has to be broken before you can use it?", "answer": "egg"},
    {"q": "What invention lets you look right through a wall?", "answer": "window"},

    # Aptitude / Trick
    {"q": "A farmer has 17 sheep. All but 9 run away. How many are left?", "answer": "9"},
    {"q": "If you divide 30 by half and add 10, what do you get?", "answer": "70"},
    {"q": "A man buys a $20 book and gives a $50 note. Change?", "answer": "30"},
    {"q": "If you have only one match and enter a dark room with an oil lamp, a candle, and a stove, what do you light first?", "answer": "match"},
]

# -------------------
# MAIN APP
# -------------------
st.title("🧠 Obed’s Daily Puzzle Challenge")
st.markdown("Solve up to **5 puzzles a day**, earn points, and climb the leaderboard 🚀")

# Track visits
if "visited" not in st.session_state:
    data["visits"] = data.get("visits", 0) + 1
    save_data(data)
    st.session_state.visited = True

username = st.text_input("👉 Enter your username to start:")

if username:
    today = datetime.now().strftime("%Y-%m-%d")
    player = players.get(username, {"score": 0, "last_played": None, "streak": 0, "today_count": 0})

    # Reset daily counter
    if player["last_played"] != today:
        player["today_count"] = 0

    # -------------------
    # GAME LOGIC
    # -------------------
    if player["today_count"] < 5:
        if "current_q" not in st.session_state:
            st.session_state.current_q = None

        if st.button("🎲 Get a Puzzle"):
            st.session_state.current_q = random.choice(puzzles)

        if st.session_state.current_q:
            q = st.session_state.current_q
            st.markdown(f"### ❓ {q['q']}")
            answer = st.text_input("Your answer:", key=f"ans_{player['today_count']}")

            if st.button("✅ Submit Answer", key=f"submit_{player['today_count']}"):
                if answer.strip().lower() == q["answer"].lower():
                    st.success("🎉 Correct! +10 points")
                    player["score"] += 10
                else:
                    st.error(f"❌ Wrong! The correct answer is **{q['answer']}**.")

                player["today_count"] += 1
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                if player.get("last_played") == yesterday:
                    player["streak"] += 1
                elif player["today_count"] == 1:
                    player["streak"] = 1
                player["last_played"] = today

                players[username] = player
                data["players"] = players
                save_data(data)

                st.session_state.current_q = None

    else:
        st.warning("⏳ You’ve answered 5 puzzles today. Come back tomorrow!")

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

    st.markdown("---")
    st.info(f"👀 Total site visits: {data.get('visits', 0)}") 

