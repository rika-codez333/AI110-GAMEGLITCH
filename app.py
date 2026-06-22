import random
import streamlit as st
from logic_utils import (
    get_range_for_difficulty, parse_guess, check_guess, update_score
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# ---------------------------------------------------------------------------
# Sidebar: difficulty settings
# ---------------------------------------------------------------------------

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 7,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# Reset the game when the selected difficulty changes.
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------------------
# Guess history sidebar
# ---------------------------------------------------------------------------

history = st.session_state.get("history", [])
valid_guesses = [g for g in history if isinstance(g, int)]
if valid_guesses:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📜 Guess History")
    secret = st.session_state.get("secret", 0)
    range_size = high - low or 1
    for i, guess in enumerate(valid_guesses, start=1):
        if guess == secret:
            icon, result = "✅", "Correct!"
        elif guess > secret:
            icon, result = "⬇️", "Too High"
        else:
            icon, result = "⬆️", "Too Low"
        closeness = 1.0 - min(abs(guess - secret) / range_size, 1.0)
        temp = "🔥" if closeness >= 0.8 else ("♨️" if closeness >= 0.4 else "🧊")
        st.sidebar.markdown(f"**#{i}** `{guess}` {icon} {result} {temp}")
        st.sidebar.progress(closeness)

# ---------------------------------------------------------------------------
# Debug panel
# ---------------------------------------------------------------------------

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ---------------------------------------------------------------------------
# Main game area
# ---------------------------------------------------------------------------

st.subheader("Make a guess")

attempts_left = attempt_limit - st.session_state.attempts

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

guess_text = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)

with col1:
    submit = st.button("Submit Guess 🚀")

with col2:
    new_game = st.button("New Game 🔁")

with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ---------------------------------------------------------------------------
# New game
# ---------------------------------------------------------------------------

if new_game:
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.secret = random.randint(low, high)
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

# Stop here if the round has already ended.

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# Handle a submitted guess.

if submit:
    success, guess_int, error_message = parse_guess(guess_text)

    if not success:
        st.session_state.history.append(guess_text)
        st.error(error_message)

    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, hint_message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(hint_message)
            if outcome != "Win":
                distance = abs(guess_int - st.session_state.secret)
                range_size = high - low or 1
                closeness = 1.0 - min(distance / range_size, 1.0)
                if closeness >= 0.8:
                    proximity_msg = "🔥 Very close!"
                elif closeness >= 0.5:
                    proximity_msg = "♨️ Getting warm!"
                elif closeness >= 0.3:
                    proximity_msg = "🌡️ Lukewarm..."
                else:
                    proximity_msg = "🧊 Way off!"
                st.caption(proximity_msg)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )

        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

        st.rerun()

st.divider()
st.caption("Built with Streamlit and a little help from AI.")
