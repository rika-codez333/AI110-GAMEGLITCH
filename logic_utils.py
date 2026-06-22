def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for the given difficulty."""

    if difficulty == "Easy":
        return 1, 20

    if difficulty == "Normal":
        # FIX: was (1, 100) — Normal and Hard ranges were swapped.
        return 1, 50

    if difficulty == "Hard":
        # FIX: was (1, 50) — corrected Hard to the wider range.
        return 1, 100

    return 1, 100


def parse_guess(raw: str):
    """
    Parse the player's raw text input into an integer guess.

    Returns a tuple of (success, parsed_integer, error_message).
    On success: (True,  integer_value, None)
    On failure: (False, None,          error string)
    """

    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        # Accept decimal input like "7.0" by rounding toward zero.
        if "." in raw:
            parsed_value = int(float(raw))
        else:
            parsed_value = int(raw)

    except Exception:
        return False, None, "That is not a number."

    return True, parsed_value, None


def check_guess(guess, secret):
    """
    Compare the player's guess to the secret number.

    Returns (outcome, hint_message) where outcome is one of:
        "Win"      -- guess matches secret
        "Too High" -- guess is above secret
        "Too Low"  -- guess is below secret
    """

    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        # FIX: was "Go HIGHER!" — reversed hint when guess was too high.
        return "Too High", "📉 Go LOWER!"

    # FIX: was "Go LOWER!" — reversed hint when guess was too low.
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate the new score after a guess.

    attempt_number is 1-indexed (first guess = 1, second = 2, ...).
    Win scoring:   start at 100 points, subtract 10 per attempt already used.
                   Minimum win award is always 10 points.
    Wrong guesses: Too High on an even attempt awards 5 pts (direction bonus).
                   All other wrong guesses deduct 5 pts.
    """

    if attempt_number < 1:
        # FIX: guard added; 0 or negative silently awarded inflated points.
        raise ValueError(
            f"attempt_number must be >= 1, got {attempt_number}"
        )

    if outcome == "Win":
        # FIX: removed +1 off-by-one; first-guess win was scoring 80 not 90.
        points_awarded = max(100 - 10 * attempt_number, 10)
        return current_score + points_awarded

    if outcome == "Too High":
        bonus = attempt_number % 2 == 0
        return current_score + 5 if bonus else current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
