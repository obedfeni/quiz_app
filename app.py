import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase using secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------------
# CONFIG
# -------------------
st.set_page_config(
    page_title="Obed’s Puzzle Challenge 🧩",
    page_icon="🧠",
    layout="centered"
)

# Hide Streamlit chrome (menu, footer, header)
_hide_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(_hide_style, unsafe_allow_html=True)

# Blue & White custom theme
_custom_style = """
<style>
html, body, .stApp { background: #f0f6ff; color: #0d1b2a; }
h1, h2, h3, h4, h5 { color: #1e3a8a; }
.stButton>button {
  background: #2563eb; color: #fff; border: none; border-radius: 12px;
  padding: .6em 1.1em; font-weight: 600;
}
.stButton>button:hover { background: #1e40af; }
.stTextInput>div>div>input {
  border: 1px solid #2563eb; border-radius: 10px; padding: .55em .7em;
}
.block-card {
  background: #ffffff; border-radius: 14px; padding: 16px 18px;
  box-shadow: 0 6px 18px rgba(0,0,0,.06); margin: 10px 0;
}
.small { color:#334155; font-size:.92rem; }
</style>
"""
st.markdown(_custom_style, unsafe_allow_html=True)

DATA_FILE = "player_data.json"
PLAYS_PER_DAY = 5
POINTS_PER_CORRECT = 10

# -------------------
# LOAD / SAVE DATA (Firestore)
# -------------------
def load_data():
    doc_ref = db.collection("game_data").document("main")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        # Initialize if not exists
        initial = {"players": {}, "visits": 0}
        doc_ref.set(initial)
        return initial

def save_data(data):
    doc_ref = db.collection("game_data").document("main")
    doc_ref.set(data)

# Load once at start
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
    {"q": "Unscramble: **FCRIAA**", "answer": "AFRICA"},
    {"q": "Unscramble: **AIASS**", "answer": "ASIA"},
    {"q": "Unscramble: **EORUP**", "answer": "EUROPE"},
    {"q": "Unscramble: **ITACAOASUNRL**", "answer": "AUSTRALOCIAN → AUSTRALIA"},  
    {"q": "Unscramble: **THOANR AMRICEA**", "answer": "NORTH AMERICA"},
    {"q": "Unscramble: **SOTHU AMRICEA**", "answer": "SOUTH AMERICA"},
    {"q": "Unscramble: **ACTTACANRIA**", "answer": "ANTARCTICA"},
    {"q": "Unscramble: **ACANAD**", "answer": "CANADA"},{"q": "Unscramble: **NIDIA**", "answer": "INDIA"},
    {"q": "Unscramble: **APANJ**", "answer": "JAPAN"},
{"q": "Unscramble: **NAMREY**", "answer": "GERMANY"},
{"q": "Unscramble: **ZILBAR**", "answer": "BRAZIL"},
{"q": "Unscramble: **FGNRAEC**", "answer": "FRANCE"},
{"q": "Unscramble: **XOCEMI**", "answer": "MEXICO"},
{"q": "Unscramble: **GKORAE**", "answer": "KOREA"},
{"q": "Unscramble: **SITAUARL**", "answer": "AUSTRALIA"},
{"q": "Unscramble: **EYPTG**", "answer": "EGYPT"},
{"q": "Unscramble: **ANIPSE**", "answer": "SPAIN"},
{"q": "Unscramble: **KNUAYR**", "answer": "UKRAINE"},
{"q": "Unscramble: **GTLUAORE**", "answer": "PORTUGAL"},
{"q": "Unscramble: **ANZIMBAWE**", "answer": "ZIMBABWE"},
{"q": "Unscramble: **RUSASIA**", "answer": "RUSSIA"},
{"q": "Unscramble: **NILEGDNA**", "answer": "ENGLAND"},
{"q": "Unscramble: **NEDALSWRIT**", "answer": "SWITZERLAND"},
{"q": "Unscramble: **NDAALHETRS**", "answer": "NETHERLANDS"},
{"q": "Unscramble: **RAQAAT**", "answer": "QATAR"},
{"q": "Unscramble: **ARCSAINH**", "answer": "CHINA"},



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
# HEADER
# -------------------
st.markdown(
    """
    <div class="block-card" style="text-align:center;">
      <h1>🧠 Obed’s Daily Puzzle Challenge</h1>
      <p class="small">Solve up to <b>5 puzzles per day</b>. Each correct answer is <b>+10 points</b>. Keep your streak and climb the leaderboard 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Count one visit per browser session
if "counted_visit" not in st.session_state:
    data["visits"] = data.get("visits", 0) + 1
    save_data(data)
    st.session_state.counted_visit = True

# -------------------
# USERNAME
# -------------------
username = st.text_input("👉 Enter your username to start:")

if not username:
    st.stop()

# Ensure player record exists
if username not in players:
    players[username] = {"score": 0, "last_played": None, "streak": 0, "today_count": 0}
    data["players"] = players
    save_data(data)

player = players[username]
today = datetime.now().strftime("%Y-%m-%d")

# Reset today's counter if new day
if player.get("last_played") != today:
    player["today_count"] = 0

# -------------------
# SESSION STATE (always store full puzzle dict)
# -------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = None  # will hold {'q':..., 'answer':...}
if "q_session_id" not in st.session_state:
    st.session_state.q_session_id = 0  # used to reset input widgets

# -------------------
# GAME LOGIC
# -------------------
remaining = max(0, PLAYS_PER_DAY - player["today_count"])
st.markdown(f"<div class='block-card'><b>🗓️ Daily plays left:</b> {remaining} / {PLAYS_PER_DAY}</div>", unsafe_allow_html=True)

if remaining == 0:
    st.warning("⏳ You’ve answered your 5 puzzles today. Come back tomorrow!")
else:
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("🎲 Get a Puzzle"):
            st.session_state.current_q = random.choice(puzzles)   # store the full dict
            st.session_state.q_session_id += 1                    # refresh input widget

    # Show puzzle if present
    if st.session_state.current_q:
        qobj = st.session_state.current_q
        # Defensive: handle both dict or stray string (from older state)
        if isinstance(qobj, dict):
            q_text = qobj.get("q", "")
            correct_answer = qobj.get("answer", "")
        else:
            q_text = str(qobj)
            correct_answer = str(st.session_state.get("current_a", ""))

        st.markdown(f"<div class='block-card'><h3>❓ {q_text}</h3></div>", unsafe_allow_html=True)

        user_answer = st.text_input(
            "Your answer:",
            key=f"ans_{st.session_state.q_session_id}",
            placeholder="Type your answer here"
        )

        if st.button("✅ Submit Answer", key=f"submit_{st.session_state.q_session_id}"):
            # Evaluate (case-insensitive, trim spaces)
            if user_answer.strip().lower() == str(correct_answer).strip().lower():
                st.success(f"🎉 Correct! +{POINTS_PER_CORRECT} points")
                player["score"] += POINTS_PER_CORRECT
            else:
                st.error(f"❌ Wrong! The correct answer is **{correct_answer}**.")

            # Update counters & streaks
            previously_played = player.get("last_played")
            player["today_count"] += 1
            player["last_played"] = today

            if previously_played == (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"):
                player["streak"] = player.get("streak", 0) + 1
            elif player["today_count"] == 1:
                player["streak"] = 1

            # Persist
            players[username] = player
            data["players"] = players
            save_data(data)

            # Clear current puzzle
            st.session_state.current_q = None

            # If limit reached, notify
            if player["today_count"] >= PLAYS_PER_DAY:
                st.warning("⏳ That was your last puzzle for today. Come back tomorrow!")

# -------------------
# LEADERBOARD
# -------------------
st.markdown("----")
st.subheader("🏆 Leaderboard")
if players:
    leaderboard = sorted(players.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    for i, (name, pdata) in enumerate(leaderboard[:10], start=1):
        st.markdown(
            f"<div class='block-card'><b>{i}. {name}</b> — {pdata.get('score',0)} pts "
            f"&nbsp;|&nbsp; 🔥 Streak: {pdata.get('streak',0)} days</div>",
            unsafe_allow_html=True
        )
else:
    st.caption("No players yet. Be the first to play!")

# -------------------
# FOOTER STATS
# -------------------
st.markdown("----")
st.info(f"👀 Total site visits: {data.get('visits', 0)}")
    # -------------------
    # SHAREABLE RESULTS
    # -------------------
if username in players:
        share_text = f"🧠 I scored {players[username]['score']} pts with a 🔥 streak of {players[username]['streak']} days in Obed’s Puzzle Challenge! Try to beat me!"
        st.text_area("📢 Share your results:", share_text, height=100) 
        st.markdown("👉 Copy this text and post on **Bluesky, Snapchat, Twitter, or WhatsApp**!")
    # Example values
username = "Obed"
score = 40
streak = 1

share_message = f"🧠 I scored {score} pts with a 🔥 streak of {streak} days in {username}’s Puzzle Challenge! Try to beat me!\n👉 https://answermufasaquestions.streamlit.app/"

st.success("🎉 Game Over! Here’s your share message:")

# Display the message
st.code(share_message, language="")

# Optional: one-click copy button
st.button("📋 Copy Message", on_click=lambda: st.session_state.update({"copy_text": share_message}))










