from logic_utils import check_guess


# ---------------------------------------------------------------------------
# Starter tests (fixed: check_guess returns a tuple, not a bare string)
# ---------------------------------------------------------------------------

def test_winning_guess():
    # Secret 50, guess 50 → Win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # Secret 50, guess 60 → Too High
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # Secret 50, guess 40 → Too Low
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug-targeted tests: even-attempt string-secret conversion
#
# The bug in app.py passed str(secret) to check_guess on every even attempt.
# Inside check_guess, comparing int vs str raises TypeError, which falls into
# the except block and uses lexicographic string comparison. Lexicographic
# ordering is wrong for numbers, e.g. "9" > "50" even though 9 < 50.
# ---------------------------------------------------------------------------

def test_string_secret_win_still_detected():
    # Even when secret is accidentally a string, an exact match should still win.
    outcome, _ = check_guess(50, "50")
    assert outcome == "Win"


def test_string_secret_causes_wrong_too_high():
    # The bug: 9 < 50 numerically → should be "Too Low".
    # But with string secret "50", lexicographic "9" > "50" → returns "Too High".
    # This test documents the buggy behavior when str(secret) is passed.
    outcome, _ = check_guess(9, "50")
    assert outcome == "Too High"  # wrong answer — reveals the string-comparison bug


def test_int_secret_correct_too_low():
    # With a proper int secret, 9 < 50 → correctly "Too Low".
    # This is the fixed behavior after app.py stopped casting secret to str.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_string_secret_causes_wrong_too_low():
    # Another lexicographic inversion: 20 > 9 numerically → "Too High".
    # But with string secret "9", "20" < "9" lexicographically → "Too Low".
    outcome, _ = check_guess(20, "9")
    assert outcome == "Too Low"  # wrong answer — reveals the string-comparison bug


def test_int_secret_correct_too_high():
    # With a proper int secret, 20 > 9 → correctly "Too High".
    outcome, _ = check_guess(20, 9)
    assert outcome == "Too High"
