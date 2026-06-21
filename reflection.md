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
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
