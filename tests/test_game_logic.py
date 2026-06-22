import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# Range selection


def test_bug1_normal_range_is_1_to_50():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50), (
        f"Normal range should be (1, 50), got ({low}, {high})"
    )


def test_bug1_hard_range_is_1_to_100():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100), (
        f"Hard range should be (1, 100), got ({low}, {high})"
    )


def test_bug1_easy_range_unchanged():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)


def test_bug1_normal_and_hard_ranges_are_not_equal():
    normal_high = get_range_for_difficulty("Normal")[1]
    hard_high = get_range_for_difficulty("Hard")[1]
    assert normal_high < hard_high, (
        "Normal upper bound must be smaller than Hard upper bound"
    )


def test_bug2_easy_upper_bound_is_not_hardcoded_100():
    _, high = get_range_for_difficulty("Easy")
    assert high == 20, f"Easy upper bound must be 20, not {high}"


def test_bug2_normal_upper_bound_is_not_hardcoded_100():
    _, high = get_range_for_difficulty("Normal")
    assert high == 50, f"Normal upper bound must be 50, not {high}"


def test_bug2_each_difficulty_produces_distinct_upper_bound():
    highs = {
        d: get_range_for_difficulty(d)[1]
        for d in ("Easy", "Normal", "Hard")
    }
    assert len(set(highs.values())) == 3, (
        f"Each difficulty must have a unique upper bound; got {highs}"
    )


# Hint messages


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
    # Cross-check that the two wrong-guess hints point in opposite directions.
    _, hint_high = check_guess(99, 1)
    _, hint_low = check_guess(1, 99)
    assert "LOWER" in hint_high, f"Too High must say LOWER, got: '{hint_high}'"
    assert "HIGHER" in hint_low, f"Too Low must say HIGHER, got: '{hint_low}'"


def test_bug4_string_secret_raises_type_error():
    with pytest.raises(TypeError):
        check_guess(80, "50")


def test_bug4_integer_comparison_not_swapped_on_even_like_inputs():
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"


# Scoring


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
    score = update_score(0, "Win", 50)
    assert score == 10


def test_bug9_zero_attempt_raises_value_error():
    with pytest.raises(ValueError):
        update_score(0, "Win", 0)


def test_bug9_negative_attempt_raises_value_error():
    with pytest.raises(ValueError):
        update_score(0, "Win", -5)


def test_bug9_error_message_includes_bad_value():
    with pytest.raises(ValueError, match="-3"):
        update_score(100, "Win", -3)


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Extra input cases


def test_c1_negative_number_parses_successfully():
    success, value, error = parse_guess("-5")
    assert success is True
    assert value == -5
    assert error is None


def test_c1_negative_guess_returns_too_low():
    outcome, hint = check_guess(-5, 10)
    assert outcome == "Too Low"
    assert hint == "📈 Go HIGHER!"


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


def test_c1_large_number_parses_successfully():
    success, value, error = parse_guess("999999")
    assert success is True
    assert value == 999999
    assert error is None


def test_c1_large_guess_returns_too_high():
    outcome, hint = check_guess(999999, 50)
    assert outcome == "Too High"
    assert hint == "📉 Go LOWER!"
