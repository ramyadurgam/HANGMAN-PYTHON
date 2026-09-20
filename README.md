CodeAlpha_Hangman

A colourful, text-based Hangman game built for the CodeAlpha Python Programming Internship (Task 1).

Features
Big ASCII title screen and a boxed "How to play" panel
Hangman that draws itself part by part (and gets an X face when you lose)
Live A-Z keyboard: green = correct, red = wrong, dim = unused
Lives shown as hearts (♥ ♥ ♥ ♡ ♡ ♡)
5 coding-themed words chosen randomly with random, each with a category
Optional hint (costs 1 life, once per round)
Guess a single letter or the whole word
Input validation: rejects numbers, symbols and repeated letters
Scoreboard with win streak, and a play-again option
Words never repeat until all 5 have been used (shuffled deck)
Screen refreshes every turn; set NO_COLOR=1 for plain text
Concepts Used

random | while loops | if / elif / else | strings | lists | functions

How to Run
bash
python hangman.py

Requires Python 3.6+ and a modern terminal (Windows Terminal, VS Code, macOS/Linux terminal). No external libraries.

How to Play
Input	Action
a single letter	guess that letter
a full word	guess the whole word (wrong = -1 life)
hint	show a clue (-1 life, once per round)
quit	leave the game
Sample Screen
  ╔════╤          
  ║    │          CATEGORY  Programming Language
  ║    O          
  ║   /|          WORD      P Y T _ _ _
  ║               
  ║               LIVES     ♥ ♥ ♥ ♡ ♡ ♡
══╩═══════        MISSED    Z Q

      Q W E R T Y U I O P
       A S D F G H J K L
         Z X C V B N M

  CLUE ▸ Named after a British comedy group, not a snake.
  Nice! 't' appears 1 time(s).
Project Structure
CodeAlpha_Hangman/
├── hangman.py
└── README.md
👤 Author
Your Name: RAMYA DURGAM

