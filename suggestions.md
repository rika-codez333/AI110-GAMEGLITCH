# Suggestions / Future Improvements

## Refactor pure logic into `logic_utils.py` (not yet done)

**Suggested:** 2026-06-21

### Problem
`app.py` runs Streamlit code at import time (`st.set_page_config`, `st.sidebar.selectbox`,
`st.columns`, etc.). This means the pure game-logic functions can't be imported in isolation.
`test_ranges.py` currently has to stub out the `streamlit` module — configuring `selectbox`,
`checkbox`, and `columns` mocks — just to test a simple function.

### Suggestion
Move the pure, UI-free functions out of `app.py` and into `logic_utils.py` (the file already
has stubs for them):

- `get_range_for_difficulty(difficulty)`
- `parse_guess(raw)`
- `check_guess(guess, secret)`
- `update_score(current_score, outcome, attempt_number)`

Then have `app.py` import them from `logic_utils`.

### Benefits
- Tests need **no Streamlit mocking**. The whole test reduces to plain assertions, e.g.:

  ```python
  from logic_utils import get_range_for_difficulty as f
  assert f("Easy")   == (1, 20)
  assert f("Normal") == (1, 50)
  assert f("Hard")   == (1, 100)
  ```

- A one-line sanity check works from the shell:

  ```bash
  python3 -c "from logic_utils import get_range_for_difficulty as f; print(f('Easy'), f('Normal'), f('Hard'))"
  ```

- Cleaner separation of game logic from UI.

### Status
Deferred — confirmed not to do this yet (2026-06-21).

---

## Latent bug: lexicographic comparison in `check_guess` string fallback (not yet fixed)

**Suggested:** 2026-06-21

### Problem
On every even-numbered attempt, `app.py` casts the secret to a string before calling
`check_guess` ([app.py:158-162](app.py#L158-L162)):

```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
else:
    secret = st.session_state.secret
```

When `secret` is a string, `guess > secret` raises `TypeError` and falls into the except
branch ([app.py:41-47](app.py#L41-L47)), which compares `str(guess)` to `secret`
lexicographically. String comparison orders by character code, not numeric value, so
multi-digit numbers sort incorrectly — e.g. `"9" > "50"` is `True` because `"9" > "5"`,
meaning a guess of `9` against a secret of `50` would be called "Too High" when it is
actually lower.

### Suggestion
Remove the string cast entirely — keeping `secret` as an int on all attempts:

```python
secret = st.session_state.secret  # always int
```

The `TypeError` fallback branch in `check_guess` would then become unreachable and can
be removed as well. This also makes the string-fallback test
(`test_string_secret_fallback_too_high_returns_go_lower`) obsolete.

### Status
Documented only — no changes made yet.

---

## Bug: New Game does not reset `status`, and `attempts` initializes to `1` instead of `0`

**Suggested:** 2026-06-21

### Problem
Two related issues in `app.py`:

1. **Missing `status` reset in the New Game handler** ([app.py:72-76](app.py#L72-L76)):
   ```python
   if new_game:
       st.session_state.attempts = 0
       st.session_state.secret = random.randint(low, high)
       st.success("New game started.")
       st.rerun()
   ```
   `st.session_state.status` is never reset to `"playing"`. After a win or loss the
   status stays `"won"` or `"lost"`, so the `st.stop()` at line 83 fires immediately
   after rerun and the new game is unplayable.

2. **`attempts` initializes to `1` instead of `0`** ([app.py:34](app.py#L34)):
   ```python
   if "attempts" not in st.session_state:
       st.session_state.attempts = 1
   ```
   The first submit increments this to `2`, so the "Attempts left" display is off by one
   from the start, and `attempt_number` passed to `update_score` is one higher than
   intended throughout the game.

### Suggestion
In the New Game handler, add `st.session_state.status = "playing"` alongside the other
resets. Also change the initial value of `attempts` to `0` to be consistent with the
New Game reset:

```python
# initial state
if "attempts" not in st.session_state:
    st.session_state.attempts = 0   # was 1

# New Game handler
if new_game:
    st.session_state.attempts = 0
    st.session_state.status = "playing"   # add this line
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()
```

### Status
Documented only — no changes made yet.

---

## Related observations (range change side effects)

- Normal got easier (1-100 -> 1-50); Hard got harder (1-50 -> 1-100).
- Hard allows only 5 attempts over a 1-100 range — verify it's still winnable
  (optimal binary search needs ~7 guesses).
- Switching difficulty mid-game updates the displayed range but not the existing
  secret until "New Game" is pressed (secret is only set when absent from session state).
