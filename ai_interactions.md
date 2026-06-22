# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Sonnet 4.6 to investigate the broken number-guessing game, identify all bugs in `app.py` and `logic_utils.py`, fix them, and write pytest tests to verify each fix.

**What did the agent do?**

1. Read `app.py` and `logic_utils.py` to map the full codebase structure.
2. Identified four bugs: swapped difficulty ranges (Bug 1), hardcoded range values (Bug 2), reversed hint messages in `check_guess` (Bug 3), `str()` coercion of the secret on even attempts (Bug 4), an off-by-one in `update_score` (Bug 8), and missing input validation on `attempt_number` (Bug 9).
3. Edited `logic_utils.py` to fix the range swap, hint logic, score formula, and add a `ValueError` guard.
4. Edited `app.py` to remove the `str()` coercion and fix the hardcoded range.
5. Wrote `tests/test_game_logic.py` with 23 named tests covering all fixed bugs, then ran `pytest` to confirm all passed.

**What did you have to verify or fix manually?**

The agent initially diagnosed the reversed hints as being caused by the attempt counter logic rather than the `str()` coercion. I had to read `app.py` myself, find the `if st.session_state.attempts % 2 == 0: secret = str(...)` line, and redirect the agent to the real root cause. I also manually ran the Streamlit app after each fix to confirm the UI behavior matched the test results — for example, verifying that a guess I knew was too high now correctly said "Go LOWER!" before marking the bug closed.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| `attempt_number=0` passed to `update_score` | "What happens if attempt_number is 0 or negative? Should we test that?" | `test_bug9_zero_attempt_raises_value_error`: calls `update_score(0, "Win", 0)` and asserts `pytest.raises(ValueError)` | Yes | Before the fix, `attempt_number=0` silently awarded 100 pts. Testing for a raised exception is more trustworthy than testing a return value — a wrong return might accidentally match the default score. |
| `attempt_number=-5` passed to `update_score` | Same prompt as above | `test_bug9_negative_attempt_raises_value_error`: calls `update_score(0, "Win", -5)` and asserts `pytest.raises(ValueError)` | Yes | Negative attempt numbers produced inflated scores with no error. The guard in `update_score` now rejects any value ≤ 0, and this test confirms that. |
| String secret passed to `check_guess` | "Write a test that would have caught the silent string-comparison bug before the fix." | `test_bug4_string_secret_raises_type_error`: calls `check_guess(80, "50")` and asserts `pytest.raises(TypeError)` | Yes | Before the fix, `"80" > "50"` evaluated to `True` and silently returned the wrong outcome. Post-fix the function raises `TypeError` immediately, making the failure visible instead of silent. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Run flake8 on app.py and logic_utils.py, then fix all warnings while keeping
the code readable. Move long inline comments above the line they describe
instead of shortening them to meaninglessness.
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

- **E262 / E265** — All `#FIX:` comments (no space after `#`) were changed to `# FIX:`. This applied to every fix annotation in both files.
- **E501 (long inline comments)** — Moved long trailing comments off the end of code lines and onto a standalone `# FIX:` line directly above. This kept the explanation intact without shrinking it to one word.
- **E501 (long import)** — Wrapped the multi-name `from logic_utils import ...` into parentheses across two lines.
- **W291 (trailing whitespace)** — Removed the trailing space after the comment on `logic_utils.py:8`.
- **Refactor in `update_score`** — Extracted `bonus = attempt_number % 2 == 0` into its own variable so the conditional return fit within 79 characters without becoming cryptic.
- After all changes: `flake8 app.py logic_utils.py` reports zero warnings. All 23 pytest tests still pass.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

Explain why casting `secret` to a string on every even-numbered attempt caused `check_guess` to return wrong hints, and describe the most Pythonic fix. (3–5 sentences on the bug, 1–2 sentences on the fix.)

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Haiku 4.5 | Claude Sonnet 4.6 |
| **Response summary** | Identified lexicographic string comparison as the root cause. Example: `"9" > "10"` is `True` because `"9" > "1"` alphabetically, so multi-digit secrets get wrong hints. Fix: remove the conditional cast and always store `secret` as an int. | Identified both the `TypeError` (int vs str comparison raises in Python 3) and the lexicographic fallback as failure modes. Also noted that `42 == "42"` is `False`, so players could never win on even attempts. Same fix: remove the cast entirely. |
| **More Pythonic?** | Both suggested the same idiomatic fix (no branching, keep `secret` as int). Tied. | Both suggested the same idiomatic fix (no branching, keep `secret` as int). Tied. |
| **Clearer explanation?** | Clear and concise — one good example, easy to follow. | More thorough — caught an extra failure mode (the `==` check always failing) that Haiku missed. |

**Which did you prefer and why?**

Sonnet for correctness: it caught that `42 == "42"` is `False` in Python 3, meaning a player could never win on an even-numbered attempt — not just get wrong hints. That's a more complete picture of the bug's impact. Haiku's response was easier to read at a glance, but the missing detail would leave a false impression that the only problem was reversed hints.
