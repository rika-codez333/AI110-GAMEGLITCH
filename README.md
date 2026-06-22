# 🎮 Game Glitch Investigator: The Impossible Guesser

## Overview

This is a Streamlit number guessing game. The player chooses a difficulty, types guesses, and gets hints about whether the secret number is higher or lower. The app also tracks attempts, score, and guess history so you can see how each round is going.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

## How To Play

1. Open the app in your browser.
2. Choose a difficulty from the sidebar.
3. Type a guess and click **Submit Guess**.
4. Use the hint to adjust your next guess.
5. Click **New Game** if you want to start a fresh round.

## What To Look For

- The sidebar shows the selected difficulty, number range, and allowed attempts.
- The main panel shows how many attempts are left.
- The guess history panel shows previous valid guesses.
- The debug panel shows the secret number, score, attempts, difficulty, and history.

## Demo Walkthrough

1. **Open the app** — launch `streamlit run app.py` and the game page opens in your browser.

2. **Pick a difficulty** — use the sidebar to choose Easy, Normal, or Hard. Each option changes the range and the number of allowed attempts.

3. **Read the range** — the message at the top tells you the correct number range for the selected difficulty.

4. **Enter a guess** — type a number and click **Submit Guess**. Invalid text shows an error and does not count as a valid guess.

5. **Read the hint** — if hints are turned on, you will see **Go LOWER!** or **Go HIGHER!** after each wrong guess.

6. **Watch your progress** — the game updates your attempts, score, and guess history as you play.

7. **Win or lose** — guessing the secret number shows a win message and balloons. Running out of attempts ends the round and reveals the secret.

8. **Start again** — click **New Game** to reset the round with a new secret number from the same difficulty range.

9. **Change difficulty anytime** — switching difficulty resets the round so the new secret always matches the new range.

10. **Check the debug panel** *(optional)* — expand "Developer Debug Info" to see the game state while testing.

**Screenshot** *(optional)*: ![fixed gameplay](fixed gameplay.png)

## Test Results

```
$ python3 -m pytest tests/test_game_logic.py
============================== 23 passed in 0.03s ==============================
```

## Stretch Features

- [x] **Challenge 4 — Enhanced Game UI:** Added hot/cold messages, a guess history sidebar, and faster debug updates in `app.py`.
- [x] **SF7 — Test Generation:** Used Claude to suggest edge-case tests for `update_score` and `check_guess`. Tests documented in `ai_interactions.md`.
- [x] **SF8 — Agent Workflow:** Asked Claude Sonnet 4.6 to investigate the game, fix the bugs, and write pytest tests. Documented in `ai_interactions.md`.
- [x] **SF9 — Linting & Style:** Ran `flake8` on `app.py` and `logic_utils.py` and fixed the warnings. Documented in `ai_interactions.md`.
- [x] **Challenge 5 / SF11 — Model Comparison:** Compared Claude Haiku 4.5 and Claude Sonnet 4.6 on the same bug-fixing task. Documented in `ai_interactions.md`.
