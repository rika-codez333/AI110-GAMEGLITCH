import pytest
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# --- Bug 1: Normal and Hard difficulty ranges were swapped ---

def test_bug1_normal_range_is_1_to_50():
    # Before fix: Normal incorrectly returned (1, 100)
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50), f"Normal range should be (1, 50), got ({low}, {high})"

def test_bug1_hard_range_is_1_to_100():
    # Before fix: Hard incorrectly returned (1, 50)
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100), f"Hard range should be (1, 100), got ({low}, {high})"

def test_bug1_easy_range_unchanged():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

def test_bug1_normal_and_hard_ranges_are_not_equal():
    # If they were still swapped they'd be identical in the wrong direction;
    # this confirms they are distinct and ordered correctly.
    normal_high = get_range_for_difficulty("Normal")[1]
    hard_high = get_range_for_difficulty("Hard")[1]
    assert normal_high < hard_high, "Normal upper bound must be smaller than Hard upper bound"

# --- Bug 2: Range was hardcoded to (1, 100) instead of using get_range_for_difficulty ---

def test_bug2_easy_upper_bound_is_not_hardcoded_100():
    # Before fix: the st.info prompt and New Game handler always used 100 regardless of difficulty.
    # get_range_for_difficulty is the single source of truth; Easy must cap at 20, not 100.
    _, high = get_range_for_difficulty("Easy")
    assert high == 20, f"Easy upper bound must be 20, not {high}"

def test_bug2_normal_upper_bound_is_not_hardcoded_100():
    _, high = get_range_for_difficulty("Normal")
    assert high == 50, f"Normal upper bound must be 50, not {high}"

def test_bug2_each_difficulty_produces_distinct_upper_bound():
    # If the range were still hardcoded to 100 everywhere, all three would return 100.
    highs = {d: get_range_for_difficulty(d)[1] for d in ("Easy", "Normal", "Hard")}
    assert len(set(highs.values())) == 3, (
        f"Each difficulty must have a unique upper bound; got {highs}"
    )

# --- Bug 3: Reversed hint messages in check_guess ---
# Before fix: "Too High" showed "Go HIGHER!" and "Too Low" showed "Go LOWER!" — players
# were told to move in the wrong direction on every wrong guess.

def test_bug3_too_high_hint_says_go_lower():
    outcome, hint = check_guess(60, 50)
    assert outcome == "Too High"
    assert hint == "📉 Go LOWER!", f"Too High hint was wrong: '{hint}'"

def test_bug3_too_low_hint_says_go_higher():
    outcome, hint = check_guess(40, 50)
    assert outcome == "Too Low"
    assert hint == "📈 Go HIGHER!", f"Too Low hint was wrong: '{hint}'"

def test_bug3_win_hint_is_correct():
    outcome, hint = check_guess(50, 50)
    assert outcome == "Win"
    assert hint == "🎉 Correct!"

def test_bug3_hints_are_not_swapped():
    # Cross-check: the two wrong-guess hints must be distinct and each points the
    # right direction — if they were still swapped, Go LOWER would appear on Too Low.
    _, hint_high = check_guess(99, 1)
    _, hint_low  = check_guess(1, 99)
    assert "LOWER" in hint_high, f"Too High must say LOWER, got: '{hint_high}'"
    assert "HIGHER" in hint_low,  f"Too Low must say HIGHER, got: '{hint_low}'"

# --- Bug 4: String secret caused silent reversed hints on even attempts ---
# Before fix: app.py cast secret to str() on even attempts, triggering a TypeError
# fallback in check_guess that used Python string comparison ("9" > "10" is True),
# flipping outcomes on ~50% of guesses.
# Fix: removed the coercion entirely. check_guess now raises TypeError on a str secret,
# which is the correct behaviour — it should never receive one.

def test_bug4_string_secret_raises_type_error():
    # If the old coercion path were still present this would silently return a wrong result;
    # post-fix it must raise TypeError instead.
    with pytest.raises(TypeError):
        check_guess(80, "50")

def test_bug4_integer_comparison_not_swapped_on_even_like_inputs():
    # Simulate the values that would appear on an "even attempt" scenario to confirm
    # integer comparison is always used and never silently flipped.
    outcome, _ = check_guess(9, 10)   # 9 < 10 → Too Low (string compare "9">"10" was True → Too High)
    assert outcome == "Too Low"

# --- Bug 8: Score off-by-one in update_score ---
# Before fix: formula was 100 - 10 * (attempt_number + 1), adding a phantom extra attempt.
# A first-guess win awarded 80 pts instead of 90.

def test_bug8_first_guess_win_scores_90():
    score = update_score(0, "Win", 1)
    assert score == 90, f"First-guess win should be 90, got {score}"

def test_bug8_second_guess_win_scores_80():
    score = update_score(0, "Win", 2)
    assert score == 80, f"Second-guess win should be 80, got {score}"

def test_bug8_ninth_guess_win_scores_minimum_10():
    score = update_score(0, "Win", 9)
    assert score == 10, f"9th-guess win should floor at 10, got {score}"

def test_bug8_win_score_does_not_go_below_10():
    # Far beyond the attempt limit — must never go negative or zero.
    score = update_score(0, "Win", 50)
    assert score == 10

# --- Bug 9: No guard on invalid attempt_number ---
# Before fix: attempt_number=0 silently awarded 100 pts with no deduction;
# negative values gave even larger scores.

def test_bug9_zero_attempt_raises_value_error():
    with pytest.raises(ValueError):
        update_score(0, "Win", 0)

def test_bug9_negative_attempt_raises_value_error():
    with pytest.raises(ValueError):
        update_score(0, "Win", -5)

def test_bug9_error_message_includes_bad_value():
    with pytest.raises(ValueError, match="-3"):
        update_score(100, "Win", -3)

# --- Existing check_guess tests (fixed to unpack the (outcome, hint) tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# --- Challenge 1: Advanced Edge-Case Testing ---

# Edge Case A: Negative numbers
# A negative integer is a valid parse but always below any in-range secret;
# verifies no crash and that check_guess returns a sensible hint.

def test_c1_negative_number_parses_successfully():
    success, value, error = parse_guess("-5")
    assert success is True
    assert value == -5
    assert error is None

def test_c1_negative_guess_returns_too_low():
    outcome, hint = check_guess(-5, 10)
    assert outcome == "Too Low"
    assert hint == "📈 Go HIGHER!"

# Edge Case B: Decimal input
# Players on mobile or with autocorrect may type decimals; confirms
# truncation toward zero is consistent across positive and negative decimals.

def test_c1_decimal_truncates_toward_zero():
    success, value, error = parse_guess("7.5")
    assert success is True
    assert value == 7
    assert error is None

def test_c1_whole_decimal_parses_cleanly():
    success, value, error = parse_guess("7.0")
    assert success is True
    assert value == 7
    assert error is None

def test_c1_negative_decimal_truncates_toward_zero():
    success, value, error = parse_guess("-3.9")
    assert success is True
    assert value == -3
    assert error is None

# Edge Case C: Extremely large values
# Ensures no overflow, crash, or unexpected behavior when a player types
# a number far outside the difficulty range.

def test_c1_large_number_parses_successfully():
    success, value, error = parse_guess("999999")
    assert success is True
    assert value == 999999
    assert error is None

def test_c1_large_guess_returns_too_high():
    outcome, hint = check_guess(999999, 50)
    assert outcome == "Too High"
    assert hint == "📉 Go LOWER!"
