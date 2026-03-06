import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

ATTEMPT_LIMIT_MAP = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}


def setup_page():
    st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
    st.title("🎮 Game Glitch Investigator")
    st.caption("An AI-generated guessing game. Something is off.")


def render_sidebar():
    """Render sidebar settings and return (difficulty, attempt_limit, low, high)."""
    st.sidebar.header("Settings")
    difficulty = st.sidebar.selectbox(
        "Difficulty",
        ["Easy", "Normal", "Hard"],
        index=1,
    )
    attempt_limit = ATTEMPT_LIMIT_MAP[difficulty]
    low, high = get_range_for_difficulty(difficulty)
    st.sidebar.caption(f"Range: {low} to {high}")
    st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
    return difficulty, attempt_limit, low, high


def init_session_state(difficulty, attempt_limit, low, high):
    """Initialize or reset session state when difficulty changes."""
    difficulty_changed = st.session_state.get("difficulty") != difficulty

    if "attempts_limit" not in st.session_state:
        st.session_state.attempt_limit = attempt_limit

    if "secret" not in st.session_state or difficulty_changed:
        st.session_state.secret = random.randint(low, high)

    if "attempts" not in st.session_state or difficulty_changed:
        st.session_state.attempts = 0

    if "score" not in st.session_state or difficulty_changed:
        st.session_state.score = 0

    if "status" not in st.session_state or difficulty_changed:
        st.session_state.status = "playing"

    if "history" not in st.session_state or difficulty_changed:
        st.session_state.history = []

    st.session_state.difficulty = difficulty


def render_debug_info():
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", st.session_state.difficulty)
        st.write("History:", st.session_state.history)


def render_game_ui(low, high):
    """Render guess input and action buttons. Returns (raw_guess, submit, new_game, show_hint)."""
    st.subheader("Make a guess")
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {st.session_state.attempt_limit - st.session_state.attempts}"
    )

    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{st.session_state.difficulty}"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess 🚀")
    with col2:
        new_game = st.button("New Game 🔁")
    with col3:
        show_hint = st.checkbox("Show hint", value=True)

    return raw_guess, submit, new_game, show_hint


def handle_new_game(low, high):
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()


def check_game_over():
    """Show terminal state message and stop if game is already won/lost."""
    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("You already won. Start a new game to play again.")
        else:
            st.error("Game over. Start a new game to try again.")
        st.stop()


def handle_submit(raw_guess, show_hint, attempt_limit):
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.pending_messages = [("error", err)]
        return

    st.session_state.history.append(guess_int)

    # Bug: secret is passed as str on even attempts, breaking numeric comparison
    if st.session_state.attempts % 2 == 0:
        secret = str(st.session_state.secret)
    else:
        secret = st.session_state.secret

    outcome, message = check_guess(guess_int, secret)

    messages = []
    if show_hint:
        messages.append(("warning", message))

    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    if outcome == "Win":
        st.session_state.status = "won"
        st.session_state.show_balloons = True
        messages.append(("success",
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        ))
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        messages.append(("error",
            f"Out of attempts! "
            f"The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        ))

    st.session_state.pending_messages = messages


def main():
    setup_page()
    difficulty, attempt_limit, low, high = render_sidebar()
    init_session_state(difficulty, attempt_limit, low, high)
    raw_guess, submit, new_game, show_hint = render_game_ui(low, high)

    if new_game:
        handle_new_game(low, high)

    check_game_over()

    if submit:
        handle_submit(raw_guess, show_hint, attempt_limit)
        st.rerun()

    if st.session_state.get("show_balloons"):
        st.balloons()
        st.session_state.show_balloons = False

    for msg_type, msg in st.session_state.pop("pending_messages", []):
        if msg_type == "error":
            st.error(msg)
        elif msg_type == "warning":
            st.warning(msg)
        elif msg_type == "success":
            st.success(msg)

    render_debug_info()


    st.divider()
    st.caption("Built by an AI that claims this code is production-ready.")


main()
