def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive number range for the given difficulty level."""

    if difficulty == "Easy":
        return 1, 20

    if difficulty == "Normal":
        return 1, 50  # I caught swapped ranges: Normal was (1, 100), Hard was (1, 50) -- corrected using Claude code. 

    if difficulty == "Hard":
        return 1, 100  # I corrected Hard to (1, 100); was (1, 50) -- corrected using Claude code.

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
        return "Too High", "📉 Go LOWER!"  # fixed reversed hint: was "Go HIGHER!" when guess was already too high -- corrected using Claude code.

    return "Too Low", "📈 Go HIGHER!"  # fixed reversed hint: was "Go LOWER!" when guess was too low.


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate the new score after a guess.

    attempt_number is 1-indexed (first guess = 1, second = 2, ...).
    Win scoring:   start at 100 points, subtract 10 per attempt already used.
                   Minimum win award is always 10 points.
    Wrong guesses: Too High on an even attempt awards 5 pts (lucky direction bonus).
                   All other wrong guesses deduct 5 pts.
    """

    if attempt_number < 1:
        raise ValueError(f"attempt_number must be >= 1, got {attempt_number}")  #FIX: AI added guard; 0 or negative silently awarded inflated points.

    if outcome == "Win":
        points_awarded = max(100 - 10 * attempt_number, 10)  #FIX: AI removed extra +1 off-by-one; first-guess win was scoring 80 instead of 90. Manually verified: debug panel confirmed secret, first-guess win showed score of 90.
        return current_score + points_awarded

    if outcome == "Too High":
        return current_score + 5 if attempt_number % 2 == 0 else current_score - 5  #FIX: Manually verified even-attempt Too High awards +5; initial test hit an odd attempt causing false failure. Logic confirmed correct.

    if outcome == "Too Low":
        return current_score - 5

    return current_score
