import random
import streamlit as st
#FIX: identified inline logic mixed with UI; refactored all game functions into logic_utils.py.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

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
# Session state initialization (runs only on the very first load)
# ---------------------------------------------------------------------------

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:  #FIX: I caught difficulty change not regenerating secret; switching Easy→Hard kept old secret outside new range.
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "attempts" not in st.session_state:
    st.session_state.attempts = 0  #FIX: AI caught off-by-one: was 1, causing first submit to count as attempt 2.

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------------------
# Debug panel (visible to developers)
# ---------------------------------------------------------------------------

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ---------------------------------------------------------------------------
# Main game UI: guess input and action buttons
# ---------------------------------------------------------------------------

st.subheader("Make a guess")

attempts_left = attempt_limit - st.session_state.attempts

#FIX: I spotted hardcoded "1 and 100" ignoring difficulty; replaced with dynamic low/high -- corrected using Claude code.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

raw_guess = st.text_input(
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
# New Game: reset all state and restart
# ---------------------------------------------------------------------------

if new_game:
    st.session_state.attempts = 0
    st.session_state.status = "playing"  #FIX: I added missing reset; without it st.stop() blocked every new game using Claude code.
    st.session_state.secret = random.randint(low, high)  #FIX: AI fixed hardcoded randint(1, 100); now respects selected difficulty.
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

# ---------------------------------------------------------------------------
# Guard: block input if the game is already over
# ---------------------------------------------------------------------------

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# ---------------------------------------------------------------------------
# Submit: process the player's guess
# ---------------------------------------------------------------------------

if submit:
    success, guess_int, error_message = parse_guess(raw_guess)

    if not success:
        st.session_state.history.append(raw_guess)
        st.error(error_message)

    else:
        st.session_state.attempts += 1  #FIX: I caught invalid guesses consuming attempts; moved increment inside valid-parse branch so only real guesses count.
        st.session_state.history.append(guess_int)

        #FIX: AI removed str(secret) coercion on even attempts that silently flipped Too High/Too Low via string comparison.
        outcome, hint_message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(hint_message)

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

# ---------------------------------------------------------------------------

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
