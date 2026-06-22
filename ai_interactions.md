# AI Interactions Log

> This file records the stretch features and AI-assisted work used on the project.

---

## Agent Workflow (SF8) — Bug Fixes

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Sonnet 4.6 to inspect the number-guessing game, find the bugs in `app.py` and `logic_utils.py`, fix them, and write pytest tests for the changes.

**What did the agent do?**

1. Read `app.py` and `logic_utils.py` to understand how the game worked.
2. Found the broken range logic, reversed hints, string coercion bug, scoring off-by-one, and missing input validation.
3. Updated `logic_utils.py` to fix the pure game logic.
4. Updated `app.py` to use the correct range and keep the secret as an integer.
5. Wrote `tests/test_game_logic.py` with 23 tests and confirmed they all passed.

**What did you have to verify or fix manually?**

The agent first blamed the attempt counter for the hint bug. I checked `app.py`, found the `str()` coercion, and corrected that diagnosis. I also ran the app myself after each fix to make sure the UI matched the tests.

---

## Agent Workflow (Challenge 2) — Guess History Sidebar

> Document the agent workflow for implementing the new Guess History feature.

**What task did you give the agent?**

I asked Claude Sonnet 4.6 to plan and implement a Guess History sidebar that visualizes how close each previous guess was to the secret number, using the existing `st.session_state.history` list that was already being populated but only shown in the developer debug panel.

**Files modified:**
- `app.py` — added the Guess History sidebar

**What did the agent do?**

1. Read `app.py` to see how session state and history were already used.
2. Filtered the history so only valid numeric guesses appear in the sidebar.
3. Added a closeness score so the progress bar grows as guesses get closer to the secret.
4. Added hot/cold emoji labels to make the guess history easier to scan.
5. Used `st.session_state.get()` so the sidebar works on the first page load.

**What did you have to verify or fix manually?**

pytest cannot fully test Streamlit UI behavior, so I confirmed the sidebar by running the app and checking it directly. I manually verified:

- **History appears after a valid guess** — the live app shows the new guess in the sidebar after submit.
- **Invalid inputs are excluded** — typing gibberish does not add a numeric entry.
- **Hot/cold tiers feel correct** — the emoji labels match the distance from the secret.
- **New Game and difficulty switch clear the panel** — the sidebar resets when the game resets.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| `attempt_number=0` passed to `update_score` | "What happens if attempt_number is 0 or negative? Should we test that?" | `test_bug9_zero_attempt_raises_value_error`: calls `update_score(0, "Win", 0)` and asserts `pytest.raises(ValueError)` | Yes | Before the fix, `attempt_number=0` silently awarded 100 pts. Testing for a raised exception is more trustworthy than testing a return value — a wrong return might accidentally match the default score. |
| `attempt_number=-5` passed to `update_score` | Same prompt as above | `test_bug9_negative_attempt_raises_value_error`: calls `update_score(0, "Win", -5)` and asserts `pytest.raises(ValueError)` | Yes | Negative attempt numbers produced inflated scores with no error. The guard in `update_score` now rejects any value ≤ 0, and this test confirms that. |
| String secret passed to `check_guess` | "Write a test that would have caught the silent string-comparison bug before the fix." | `test_bug4_string_secret_raises_type_error`: calls `check_guess(80, "50")` and asserts `pytest.raises(TypeError)` | Yes | Before the fix, `"80" > "50"` evaluated to `True` and silently returned the wrong outcome. Post-fix the function raises `TypeError` immediately, making the failure visible instead of silent. |
| Negative number (`"-5"`) passed to `parse_guess` | "What edge cases could break parse_guess or check_guess? Test negative numbers." | `test_c1_negative_number_parses_successfully` + `test_c1_negative_guess_returns_too_low` | Yes | A negative integer is a valid parse but always below any in-range secret — verifies the game returns a sensible hint rather than crashing. |
| Decimal input (`"7.5"`) passed to `parse_guess` | "Test decimal string inputs to parse_guess — positive, whole, and negative decimals." | `test_c1_decimal_truncates_toward_zero` + `test_c1_whole_decimal_parses_cleanly` + `test_c1_negative_decimal_truncates_toward_zero` | Yes | Players on mobile or with autocorrect may type decimals; confirms truncation toward zero is consistent and silent across all cases. |
| Extremely large value (`"999999"`) passed to `parse_guess` | "Test an extremely large number input to parse_guess and check_guess." | `test_c1_large_number_parses_successfully` + `test_c1_large_guess_returns_too_high` | Yes | Ensures no overflow, crash, or unexpected behavior when a player types a number far outside the difficulty range. |

---

## Professional Documentation and Linting (Challenge 3)

> Document how you used AI to add docstrings and review code style.

**Prompt used:**

```
Rewrite the docstrings in logic_utils.py using Google style with Args:,
Returns:, and Raises: sections. Keep the language plain and readable for
a beginner.
```

**Changes applied:**

- All four functions now have structured docstrings with `Args:` and `Returns:` sections.
- `get_range_for_difficulty` explains the available ranges and the fallback case.
- `parse_guess` explains how text input becomes an integer.
- `check_guess` explains how the game compares a guess with the secret.
- `update_score` explains the scoring rules and invalid attempt numbers.

**Linting output after:**

```
$ python3 -m flake8 logic_utils.py app.py
(no output — zero warnings)
```

**Verification:**

```
$ python3 -c "from logic_utils import update_score; help(update_score)"
```

Confirmed the structured docstrings render correctly in the terminal help output.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Run flake8 on app.py and logic_utils.py, then fix all warnings while keeping
the code readable.
```

**Linting output before:**

```
app.py:3:1: E265 block comment should start with '# '
app.py:3:80: E501 line too long (95 > 79 characters)
app.py:4:80: E501 line too long (88 > 79 characters)
app.py:49:48: E262 inline comment should start with '# '
app.py:49:80: E501 line too long (159 > 79 characters)
app.py:57:36: E262 inline comment should start with '# '
app.py:57:80: E501 line too long (113 > 79 characters)
app.py:87:1: E265 block comment should start with '# '
app.py:87:80: E501 line too long (121 > 79 characters)
app.py:115:42: E262 inline comment should start with '# '
app.py:115:80: E501 line too long (132 > 79 characters)
app.py:116:58: E262 inline comment should start with '# '
app.py:116:80: E501 line too long (132 > 79 characters)
app.py:144:41: E262 inline comment should start with '# '
app.py:144:80: E501 line too long (160 > 79 characters)
app.py:147:9: E265 block comment should start with '# '
app.py:147:80: E501 line too long (124 > 79 characters)
logic_utils.py:2:80: E501 line too long (83 > 79 characters)
logic_utils.py:8:80: E501 line too long (118 > 79 characters)
logic_utils.py:8:119: W291 trailing whitespace
logic_utils.py:11:80: E501 line too long (98 > 79 characters)
logic_utils.py:55:80: E501 line too long (145 > 79 characters)
logic_utils.py:57:80: E501 line too long (100 > 79 characters)
logic_utils.py:67:80: E501 line too long (84 > 79 characters)
logic_utils.py:72:80: E501 line too long (149 > 79 characters)
logic_utils.py:72:81: E262 inline comment should start with '# '
logic_utils.py:75:62: E262 inline comment should start with '# '
logic_utils.py:75:80: E501 line too long (229 > 79 characters)
logic_utils.py:79:80: E501 line too long (220 > 79 characters)
logic_utils.py:79:85: E262 inline comment should start with '# '
```

**Changes applied:**

- Wrapped the long import in `app.py`.
- Removed trailing whitespace and cleaned comment formatting.
- Kept the code readable while satisfying flake8.
- After the changes, `flake8 app.py logic_utils.py` reports zero warnings and all tests still pass.

---

## Model Comparison (Challenge 5 / SF11)

> Compare two AI models on the same task.

**Task given to both models:**

Explain why casting `secret` to a string on every even-numbered attempt caused `check_guess` to return wrong hints, and describe the most Pythonic fix.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Haiku 4.5 | Claude Sonnet 4.6 |
| **Response summary** | Identified string comparison as the root cause. Example: `"9" > "10"` is `True`, so multi-digit secrets get wrong hints. Fix: remove the cast and keep `secret` as an int. | Identified both the comparison error and the fact that `42 == "42"` is `False`, so players could never win on even attempts. Same fix: remove the cast entirely. |
| **More Pythonic?** | Both suggested the same idiomatic fix (no branching, keep `secret` as int). Tied. | Both suggested the same idiomatic fix (no branching, keep `secret` as int). Tied. |
| **Clearer explanation?** | Clear and concise — one good example, easy to follow. | More thorough — caught an extra failure mode (the `==` check always failing) that Haiku missed. |

**Which did you prefer and why?**

Sonnet was the better answer because it caught that `42 == "42"` is `False` in Python 3. That meant the bug affected both hints and winning, not just the direction message.
