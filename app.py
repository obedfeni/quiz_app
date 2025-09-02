import streamlit as st
import random
import requests

# -------------------
# Config
# -------------------
st.set_page_config(
    page_title="Mufasa's Quiz 🎯",
    page_icon="🔥",
    layout="centered"
)

st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🔥 mufasa's Quiz Challenge 🔥</h1>",
    unsafe_allow_html=True
)
st.write("Choose a category, answer 3 questions, and share your score under mufasa Bluesky post 🎉")

# -------------------
# Player Counter
# -------------------
def update_player_count():
    """Update and fetch the number of players using CountAPI."""
    namespace = "obed_quiz_app"
    key = "players"
    url = f"https://api.countapi.xyz/hit/{namespace}/{key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["value"]
    except Exception:
        return None
    return None

# -------------------
# Question Bank
# -------------------
questions = {
    "Mufasa Specials": [
        {"q": "What is mufasa full name?", "a": "Obed Feni"},
        {"q": "What is mufasa African house name?", "a": "Kobby"},
        {"q": "How old is mufasa?", "a": "24"},
        {"q": "What is mufasa favorite food?", "a": "Jollof Rice"},
        {"q": "What is mufasa favorite movie?", "a": "Black Panther"},
    ],
    "History": [
        {"q": "Who was the first President of the USA?", "a": "George Washington"},
        {"q": "In which year did World War II end?", "a": "1945"},
        {"q": "Which empire built the pyramids?", "a": "Egyptians"},
    ],
    "Science": [
        {"q": "What planet is closest to the sun?", "a": "Mercury"},
        {"q": "What gas do humans need to breathe?", "a": "Oxygen"},
        {"q": "What is H2O commonly known as?", "a": "Water"},
    ],
    "Biology": [
        {"q": "What organ pumps blood through the body?", "a": "Heart"},
        {"q": "What part of the plant makes food?", "a": "Leaf"},
        {"q": "Which animal is known as the King of the Jungle?", "a": "Lion"},
    ],
    "Arts": [
        {"q": "Who painted the Mona Lisa?", "a": "Leonardo da Vinci"},
        {"q": "Shakespeare wrote 'Romeo and ___'?", "a": "Juliet"},
        {"q": "What do you call a person who plays the piano?", "a": "Pianist"},
    ],
    "Inventions": [
        {"q": "Who invented the light bulb?", "a": "Thomas Edison"},
        {"q": "Who is credited with inventing the telephone?", "a": "Alexander Graham Bell"},
        {"q": "What company created the first iPhone?", "a": "Apple"},
    ],
    "Photography": [
        {"q": "What does DSLR stand for? (short form accepted)", "a": "Digital Single Lens Reflex"},
        {"q": "Which company makes the 'EOS' camera series?", "a": "Canon"},
        {"q": "What does the 'ISO' setting control in photography?", "a": "Light sensitivity"},
    ],
    "Psychometrics": [
        {"q": "If you enjoy solving puzzles, which trait is that linked to?", "a": "Problem-solving"},
        {"q": "Introverts gain energy from?", "a": "Being alone"},
        {"q": "Extroverts gain energy from?", "a": "Being with others"},
    ]
}

# -------------------
# Category Selection
# -------------------
category = st.selectbox("🎯 Choose a category:", list(questions.keys()))

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.selected_questions = []

if st.button("Start Quiz"):
    st.session_state.quiz_started = True
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.selected_questions = random.sample(questions[category], 3)

# -------------------
# Quiz Logic
# -------------------
if st.session_state.quiz_started:
    if st.session_state.current_q < 3:
        q_data = st.session_state.selected_questions[st.session_state.current_q]
        st.subheader(f"Q{st.session_state.current_q+1}: {q_data['q']}")

        user_answer = st.text_input("✍️ Your Answer:", key=f"q{st.session_state.current_q}")
        if st.button("Submit", key=f"submit{st.session_state.current_q}"):
            if user_answer.strip().lower() == q_data["a"].lower():
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! The correct answer is {q_data['a']}")

            st.session_state.current_q += 1

    # End of Quiz
    if st.session_state.current_q >= 3:
        st.subheader("🎉 Quiz Complete!")
        st.write(f"Your Score: **{st.session_state.score}/3**")
        st.balloons()
        player_number = update_player_count()
        if player_number:
            st.markdown(f"👥 You are **Player #{player_number}** to finish the quiz!")
        st.markdown("📸 Screenshot your result and post under Obed’s Bluesky post!")
        st.session_state.quiz_started = False

