"""
Comprehensive tests for all functions in logic_utils.py:
  - get_range_for_difficulty
  - parse_guess
  - check_guess
  - update_score
"""

import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_returns_1_to_20(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal_returns_1_to_100(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard_returns_1_to_50(self):
        assert get_range_for_difficulty("Hard") == (1, 50)

    def test_unknown_string_defaults_to_1_100(self):
        assert get_range_for_difficulty("Impossible") == (1, 100)

    def test_empty_string_defaults_to_1_100(self):
        assert get_range_for_difficulty("") == (1, 100)

    def test_lowercase_easy_defaults_to_1_100(self):
        # Case-sensitive: "easy" is not "Easy"
        assert get_range_for_difficulty("easy") == (1, 100)

    def test_none_defaults_to_1_100(self):
        assert get_range_for_difficulty(None) == (1, 100)

    def test_returns_tuple_of_two_ints(self):
        low, high = get_range_for_difficulty("Easy")
        assert isinstance(low, int) and isinstance(high, int)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    # --- invalid inputs ---

    def test_none_returns_error(self):
        ok, value, msg = parse_guess(None)
        assert ok is False
        assert value is None
        assert msg == "Enter a guess."

    def test_empty_string_returns_error(self):
        ok, value, msg = parse_guess("")
        assert ok is False
        assert value is None
        assert msg == "Enter a guess."

    def test_non_numeric_string_returns_error(self):
        ok, value, msg = parse_guess("abc")
        assert ok is False
        assert value is None
        assert msg == "That is not a number."

    def test_special_chars_return_error(self):
        ok, value, msg = parse_guess("!@#")
        assert ok is False
        assert value is None
        assert msg == "That is not a number."

    def test_whitespace_only_returns_error(self):
        ok, value, msg = parse_guess("   ")
        assert ok is False
        assert value is None
        assert msg == "That is not a number."

    # --- valid integer strings ---

    def test_valid_positive_integer(self):
        ok, value, msg = parse_guess("42")
        assert ok is True
        assert value == 42
        assert msg is None

    def test_valid_zero(self):
        ok, value, msg = parse_guess("0")
        assert ok is True
        assert value == 0
        assert msg is None

    def test_valid_negative_integer(self):
        ok, value, msg = parse_guess("-10")
        assert ok is True
        assert value == -10
        assert msg is None

    def test_valid_single_digit(self):
        ok, value, msg = parse_guess("7")
        assert ok is True
        assert value == 7
        assert msg is None

    # --- decimal strings (truncated to int) ---

    def test_decimal_string_truncated(self):
        ok, value, msg = parse_guess("3.7")
        assert ok is True
        assert value == 3
        assert msg is None

    def test_decimal_string_zero_fraction(self):
        ok, value, msg = parse_guess("5.0")
        assert ok is True
        assert value == 5
        assert msg is None

    def test_negative_decimal_truncated(self):
        ok, value, msg = parse_guess("-2.9")
        assert ok is True
        assert value == -2
        assert msg is None


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    # --- winning guess ---

    def test_exact_match_returns_win(self):
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"

    def test_exact_match_win_message(self):
        outcome, message = check_guess(50, 50)
        assert "Correct" in message

    def test_win_at_boundary_low(self):
        outcome, _ = check_guess(1, 1)
        assert outcome == "Win"

    def test_win_at_boundary_high(self):
        outcome, _ = check_guess(100, 100)
        assert outcome == "Win"

    # --- guess too high ---

    def test_guess_above_secret_returns_too_high(self):
        outcome, _ = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_above_secret_message(self):
        _, message = check_guess(60, 50)
        assert "HIGHER" in message or "High" in message

    def test_guess_one_above_secret(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_guess_far_above_secret(self):
        outcome, _ = check_guess(1000, 1)
        assert outcome == "Too High"

    # --- guess too low ---

    def test_guess_below_secret_returns_too_low(self):
        outcome, _ = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_guess_below_secret_message(self):
        _, message = check_guess(40, 50)
        assert "LOWER" in message or "Low" in message

    def test_guess_one_below_secret(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"

    def test_guess_far_below_secret(self):
        outcome, _ = check_guess(1, 100)
        assert outcome == "Too Low"

    # --- return type ---

    def test_returns_tuple_of_two(self):
        result = check_guess(50, 50)
        assert isinstance(result, tuple) and len(result) == 2


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    # --- Win outcome ---

    def test_win_on_first_attempt(self):
        # attempt_number=0: points = 100 - 10*(0+1) = 90
        assert update_score(0, "Win", 0) == 90

    def test_win_on_second_attempt(self):
        # attempt_number=1: points = 100 - 10*2 = 80
        assert update_score(0, "Win", 1) == 80

    def test_win_score_adds_to_existing_score(self):
        # attempt_number=0: points=90, existing=50 → 140
        assert update_score(50, "Win", 0) == 140

    def test_win_minimum_points_clamped_to_10(self):
        # attempt_number=9: 100 - 10*10 = 0 → clamped to 10
        assert update_score(0, "Win", 9) == 10

    def test_win_minimum_points_clamped_high_attempt(self):
        # attempt_number=100: 100 - 1010 < 0 → clamped to 10
        assert update_score(0, "Win", 100) == 10

    def test_win_on_attempt_8_not_clamped(self):
        # attempt_number=8: 100 - 10*9 = 10 (exactly at clamp boundary)
        assert update_score(0, "Win", 8) == 10

    def test_win_on_attempt_7_not_clamped(self):
        # attempt_number=7: 100 - 10*8 = 20
        assert update_score(0, "Win", 7) == 20

    # --- Too High outcome ---

    def test_too_high_even_attempt_adds_5(self):
        # attempt_number=0 (even): +5
        assert update_score(100, "Too High", 0) == 105

    def test_too_high_odd_attempt_subtracts_5(self):
        # attempt_number=1 (odd): -5
        assert update_score(100, "Too High", 1) == 95

    def test_too_high_attempt_2_even_adds_5(self):
        assert update_score(50, "Too High", 2) == 55

    def test_too_high_attempt_3_odd_subtracts_5(self):
        assert update_score(50, "Too High", 3) == 45

    # --- Too Low outcome ---

    def test_too_low_always_subtracts_5(self):
        assert update_score(100, "Too Low", 0) == 95

    def test_too_low_odd_attempt_still_subtracts_5(self):
        assert update_score(100, "Too Low", 1) == 95

    def test_too_low_even_attempt_still_subtracts_5(self):
        assert update_score(100, "Too Low", 4) == 95

    # --- Unknown outcome ---

    def test_unknown_outcome_score_unchanged(self):
        assert update_score(200, "Draw", 0) == 200

    def test_empty_string_outcome_score_unchanged(self):
        assert update_score(50, "", 0) == 50

    def test_none_outcome_score_unchanged(self):
        assert update_score(75, None, 0) == 75
