def get_range_for_difficulty(difficulty: str):
    """Return the number range for a difficulty level.

    Args:
        difficulty: The selected difficulty name.

    Returns:
        A tuple of ``(low, high)`` numbers for the game range.
    """

    if difficulty == "Easy":
        return 1, 20

    if difficulty == "Normal":
        return 1, 50

    if difficulty == "Hard":
        return 1, 100

    return 1, 100


def parse_guess(raw: str):
    """Convert a typed guess into an integer when possible.

    Args:
        raw: The text entered by the player.

    Returns:
        A tuple of ``(success, value, error)``.
    """

    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            parsed_value = int(float(raw))
        else:
            parsed_value = int(raw)

    except Exception:
        return False, None, "That is not a number."

    return True, parsed_value, None


def check_guess(guess, secret):
    """Compare a guess with the secret number.

    Args:
        guess: The player's guess.
        secret: The number the player is trying to find.

    Returns:
        A tuple of ``(outcome, hint)``.
    """

    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Return the updated score after one guess.

    Scoring rules:
      - A correct guess awards 100 points minus 10 for each attempt used.
      - A "Too High" guess on an even-numbered attempt earns 5 points.
      - Any other wrong guess deducts 5 points.

    Args:
        current_score: The score before this guess.
        outcome: The result of the guess.
        attempt_number: The number of the current valid guess.

    Returns:
        The updated score.
    """

    if attempt_number < 1:
        raise ValueError(
            f"attempt_number must be >= 1, got {attempt_number}"
        )

    if outcome == "Win":
        points_awarded = max(100 - 10 * attempt_number, 10)
        return current_score + points_awarded

    if outcome == "Too High":
        bonus = attempt_number % 2 == 0
        return current_score + 5 if bonus else current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
