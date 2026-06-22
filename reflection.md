# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

    The hints were giving the wrong prompt (e.g. go higher or lower) on every number I guessed.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    1. The hints were backwards (recommending "Go Higher" for too-high guesses and vice versa).
    2. The difficulty ranges were mismatched ("Normal" had a larger range than "Hard").
    3. The secret number was being converted to a string on alternate attempts, causing faulty alphabetical string comparisons instead of integer comparisons.
    4. The attempt counter started at 1 and incremented before checking the guess, resulting in only 7 allowed attempts on Normal instead of 8.
---


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 44 (Secret: 84) | "Go Higher" hint | "Go Lower" hint | None |
| Guess of 75 (Secret: 84) | "Go Lower" hint | "Go Higher" hint | None |
| Guess of 9 (Secret: 57) on new game attempt | "Go Higher" hint | "Go Lower" hint | None (TypeError caught internally, falling back to string comparison '9' > '57' which is True) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used the Claude Sonnet 4.6 (Medium) model as my primary pair programmer to examine codebase patterns, run local test suites, and write code.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  One correct AI suggestion was that the hint bug came from the code converting the secret number to a string on alternating attempts before comparing it to the integer guess.  

    I verified this by reading 'app.py', finding the 'if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)' logic, and then reproducing the wrong hints manually: even-numbered guesses compared as strings produced backwards higher/lower feedback. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  One incorrect AI suggestion was that the broken hints were caused mainly by the attempt counter logic. I verified by inspecting app.py and found the actual misleading bug was the secret being converted to a string on alternating attempts (secret = str(st.session_state.secret)), which caused alphabetical comparisons and reversed the “higher/lower” hints. 
    
    I confirmed this by reproducing the behavior: even-numbered guesses produced wrong feedback only when the secret was compared as a string.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  A fix counted as real only when the relevant pytest test passed AND I could reproduce the correct behavior manually in the Streamlit app. For example, after fixing the reversed hints in `check_guess`, I ran the game and guessed a number I knew was too high — I confirmed it said "Go LOWER!" instead of "Go HIGHER!" before marking it done.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

  `test_bug4_string_secret_raises_type_error` (line 80–84 in `tests/test_game_logic.py`) was the most revealing. Before the fix, calling `check_guess(80, "50")` silently returned a wrong result because Python string comparison (`"80" > "50"` is `True`) produced a misleading "Too High" — no crash, no warning. After removing the `str()` coercion from `app.py`, the same call now raises a `TypeError`. The test confirmed that the silent failure mode was gone and any future accidental string secret would immediately surface as an error rather than producing wrong hints.

- Did AI help you design or understand any tests? How?

  Yes. AI suggested the guard tests for Bug 9 (`test_bug9_zero_attempt_raises_value_error`, `test_bug9_negative_attempt_raises_value_error`) — I hadn't thought to test invalid `attempt_number` values at all. It also explained why testing for a raised exception (using `pytest.raises`) is more trustworthy than testing a return value, because a wrong return value might accidentally pass if the default score happens to match. That framing helped me understand the difference between testing that code rejects bad input versus testing that it handles it quietly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Every time you interact with a Streamlit app — clicking a button, typing in a box, changing the difficulty dropdown — Streamlit reruns the entire Python script from top to bottom, as if starting fresh. That means any regular variable you set (like `attempts = 0`) gets wiped out on each rerun. `st.session_state` is Streamlit's solution: it's a special dictionary that survives across reruns, so values like `st.session_state.attempts`, `st.session_state.secret`, and `st.session_state.score` persist between interactions. In this game, that's how the secret number stays the same across multiple guesses — without session state, a new random number would be picked on every button click, making the game unwinnable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  Writing a pytest test immediately after fixing each bug, not at the end. Every fix got its own named test before I moved on, so regressions were caught instantly rather than discovered later during manual testing.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would read the relevant code myself before accepting an AI diagnosis. I wasted time chasing the attempt counter as the root cause of the hint bug when the real issue — the `str()` coercion — was visible in `app.py` and would have been obvious if I'd read it first.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI-generated code can have bugs that are silent and hard to spot — a single `str()` cast flipped the game's hints on half of all guesses with no error message. I now treat AI output like any unfamiliar code: read it, reproduce its behavior, and write a test that would have caught the bug.
