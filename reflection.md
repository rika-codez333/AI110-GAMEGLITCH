# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

    The hints pointed in the wrong direction for every guess.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    1. The hints were backwards.
    2. The difficulty ranges were mismatched.
    3. The secret number was converted to a string on alternate attempts, which caused string comparison bugs.
    4. The attempt counter started at 1, so Normal difficulty allowed only 7 guesses instead of 8.
---


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 44 (Secret: 84) | "Go Higher" hint | "Go Lower" hint | None |
| Guess of 75 (Secret: 84) | "Go Lower" hint | "Go Higher" hint | None |
| Guess of 9 (Secret: 57) on new game attempt | "Go Higher" hint | "Go Lower" hint | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude Sonnet 4.6 as my primary pair programmer to inspect the code, run tests, and help write fixes.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  One correct AI suggestion was that the hint bug came from converting the secret number to a string on alternating attempts.

    I verified this by reading `app.py`, finding the `str()` conversion, and reproducing the wrong hints manually.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  One incorrect AI suggestion was that the broken hints were caused mainly by the attempt counter logic. I checked `app.py` and found the real issue was the string conversion of the secret number.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  A fix counted as real only when the relevant pytest test passed and I could reproduce the correct behavior manually in the Streamlit app.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

  `test_bug4_string_secret_raises_type_error` in `tests/test_game_logic.py` was the most revealing. Before the fix, calling `check_guess(80, "50")` could return the wrong result because the secret was being treated like text. After removing the string conversion from `app.py`, the same call now raises a `TypeError`.

- Did AI help you design or understand any tests? How?

  Yes. AI suggested the guard tests for Bug 9 (`test_bug9_zero_attempt_raises_value_error` and `test_bug9_negative_attempt_raises_value_error`), and that helped me think about invalid input more carefully.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Every time you interact with a Streamlit app, the script runs again from the top. Regular variables are reset, but `st.session_state` keeps values between reruns. That is why this game can remember the secret number, the score, and the attempt count.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  Writing a pytest test right after fixing a bug, instead of waiting until the end.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would read the relevant code myself before accepting an AI diagnosis. It would have saved time on the hint bug.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI-generated code can have bugs that are hard to spot. I now treat AI output like any unfamiliar code: read it, reproduce it, and write a test for it.
