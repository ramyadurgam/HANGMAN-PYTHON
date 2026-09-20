"""
CodeAlpha Python Programming Internship
Task 1: Hangman Game  (Colourful Edition)
------------------------------------------------------------
A polished text-based Hangman game with a coding theme.

Rules
  * The computer picks a random word from a list of 5 words.
  * Guess one letter at a time. 6 wrong guesses and you lose.
  * Type 'hint' for a clue (costs 1 life), or guess the whole word.
  * Type 'quit' to leave the game.

Tip: colours work in most modern terminals. Set NO_COLOR=1 to switch
them off.
"""

import os
import random
import re
import sys

MAX_WRONG = 6
WIDTH = 64

# 5 predefined words: (word, category, clue)
WORDS = [
    ("python", "Programming Language", "Named after a British comedy group, not a snake."),
    ("function", "Programming Concept", "A reusable block of code you call by name."),
    ("variable", "Programming Concept", "A named box that stores a value."),
    ("algorithm", "Computer Science", "A step-by-step recipe for solving a problem."),
    ("developer", "Career", "The person who writes and fixes the code."),
]

# ------------------------------------------------------------------
#  Colour helpers
# ------------------------------------------------------------------
USE_COLOR = (sys.stdout.isatty() or "FORCE_COLOR" in os.environ) \
    and "NO_COLOR" not in os.environ

if os.name == "nt":
    os.system("")  # lets Windows terminals understand colour codes

CODES = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
}
ANSI_PATTERN = re.compile(r"\033\[[0-9;]*m")


def paint(text, *styles):
    """Wrap text in colour/style codes (does nothing if colour is off)."""
    if not USE_COLOR:
        return text
    return "".join(CODES[s] for s in styles) + text + CODES["reset"]


def visible_len(text):
    """Length of text as seen on screen (ignores colour codes)."""
    return len(ANSI_PATTERN.sub("", text))


def pad(text, width):
    return text + " " * (width - visible_len(text))


def center(text, width):
    space = width - visible_len(text)
    left = space // 2
    return " " * left + text + " " * (space - left)


def box(lines, color):
    """Draw a double-line box around a list of text lines."""
    inner = WIDTH - 2
    out = [paint("╔" + "═" * inner + "╗", color)]
    for line in lines:
        out.append(paint("║", color) + center(line, inner) + paint("║", color))
    out.append(paint("╚" + "═" * inner + "╝", color))
    return out


def clear_screen():
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")
    else:
        print("\n" + "-" * WIDTH)


# ------------------------------------------------------------------
#  Drawing helpers
# ------------------------------------------------------------------
TITLE_ART = [
    "██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗",
    "██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║",
    "███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║",
    "██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║",
    "██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║",
    "╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝",
]


def gallows_lines(mistakes, dead=False):
    """Build the gallows; a new body part appears with each mistake."""
    head = ("X" if dead else "O") if mistakes >= 1 else " "
    body = "|" if mistakes >= 2 else " "
    left_arm = "/" if mistakes >= 3 else " "
    right_arm = "\\" if mistakes >= 4 else " "
    left_leg = "/" if mistakes >= 5 else " "
    right_leg = "\\" if mistakes >= 6 else " "

    return [
        paint("  ╔════╤", "yellow"),
        paint("  ║    │", "yellow"),
        paint("  ║    ", "yellow") + paint(head, "red", "bold"),
        paint("  ║   ", "yellow") + paint(left_arm + body + right_arm, "red", "bold"),
        paint("  ║   ", "yellow") + paint(left_leg + " " + right_leg, "red", "bold"),
        paint("  ║", "yellow"),
        paint("══╩═══════", "yellow"),
    ]


def word_display(word, guessed, reveal=False):
    """Big spaced-out word. On a loss, missing letters are shown in red."""
    shown = []
    for letter in word:
        if letter in guessed:
            shown.append(paint(letter.upper(), "bold", "cyan"))
        elif reveal:
            shown.append(paint(letter.upper(), "bold", "red"))
        else:
            shown.append(paint("_", "dim"))
    return " ".join(shown)


def hearts(lives):
    parts = []
    for i in range(MAX_WRONG):
        if i < lives:
            parts.append(paint("♥", "red", "bold"))
        else:
            parts.append(paint("♡", "dim"))
    return " ".join(parts)


def keyboard_lines(guessed, wrong):
    """A-Z keyboard: green = correct, red = wrong, dim = unused."""
    rows = [("QWERTYUIOP", 0), ("ASDFGHJKL", 1), ("ZXCVBNM", 3)]
    lines = []
    for letters, indent in rows:
        keys = []
        for key in letters:
            low = key.lower()
            if low in guessed:
                keys.append(paint(key, "green", "bold"))
            elif low in wrong:
                keys.append(paint(key, "red"))
            else:
                keys.append(paint(key, "dim"))
        lines.append(" " * indent + " ".join(keys))
    return lines


def render(word, category, guessed, wrong, mistakes, header,
           message=None, clue=None, over=None):
    """Redraw the whole game screen."""
    dead = over == "lose"
    lives = MAX_WRONG - mistakes
    wrong_text = " ".join(letter.upper() for letter in wrong) if wrong else "-"

    info = [
        "",
        paint("CATEGORY  ", "dim") + paint(category, "magenta", "bold"),
        "",
        paint("WORD      ", "dim") + word_display(word, guessed, dead),
        "",
        paint("LIVES     ", "dim") + hearts(lives),
        paint("MISSED    ", "dim") + paint(wrong_text, "red"),
    ]

    clear_screen()
    print()
    for line in header:
        print(line)
    print()
    for art, text in zip(gallows_lines(mistakes, dead), info):
        print(pad(art, 18) + text)
    print()
    for line in keyboard_lines(guessed, wrong):
        print("      " + line)
    print()
    if clue:
        print("  " + paint("CLUE ▸ ", "yellow", "bold") + paint(clue, "yellow"))
    if message:
        text, color = message
        print("  " + paint(text, color, "bold"))
    print()


def make_header(round_no, wins, losses, streak):
    stats = (f"Round {paint(str(round_no), 'bold')}   "
             f"Wins {paint(str(wins), 'green', 'bold')}   "
             f"Losses {paint(str(losses), 'red', 'bold')}   "
             f"Streak {paint(str(streak), 'yellow', 'bold')}")
    title = paint("☠  H A N G M A N  ☠", "bold", "cyan") + \
        paint("   ·   CodeAlpha", "dim")
    return box([title, stats], "cyan")


def show_title():
    clear_screen()
    print()
    for line in TITLE_ART:
        print("  " + paint(line, "cyan", "bold"))
    print()
    print(center(paint("★  The Coder's Word Game  ★", "yellow", "bold"), WIDTH + 4))
    print()
    rules = [
        paint("HOW TO PLAY", "bold", "yellow"),
        "",
        "Guess the hidden word one letter at a time.",
        f"You may miss {MAX_WRONG} times before the man is hanged!",
        "",
        paint("a-z", "green", "bold") + " guess a letter    " +
        paint("hint", "yellow", "bold") + " get a clue (-1 life)",
        paint("word", "cyan", "bold") + " guess it all      " +
        paint("quit", "red", "bold") + " leave the game",
    ]
    for line in box(rules, "magenta"):
        print("  " + line)
    print()
    input("  " + paint("Press ENTER to start ▸ ", "green", "bold"))


# ------------------------------------------------------------------
#  Game logic
# ------------------------------------------------------------------
def is_solved(word, guessed):
    """True when every letter of the word has been guessed."""
    for letter in word:
        if letter not in guessed:
            return False
    return True


def play_round(word, category, clue, header):
    """Play one game. Returns 'win', 'lose' or 'quit'."""
    guessed = []       # correct letters
    wrong = []         # wrong letters
    mistakes = 0
    hint_used = False
    message = (f"A new word! It has {len(word)} letters. Good luck!", "yellow")

    while mistakes < MAX_WRONG and not is_solved(word, guessed):
        render(word, category, guessed, wrong, mistakes, header, message,
               clue if hint_used else None)
        guess = input("  " + paint("➤ Your guess: ", "cyan", "bold")).strip().lower()

        if guess == "quit":
            print(f"\n  You left the game. The word was '{word.upper()}'.")
            return "quit"

        elif guess == "hint":
            if hint_used:
                message = ("You already used your hint!", "yellow")
            elif mistakes >= MAX_WRONG - 1:
                message = ("Too risky! A hint would cost your last life.", "yellow")
            else:
                hint_used = True
                mistakes += 1
                message = ("Hint unlocked!  (-1 life)", "yellow")

        elif not guess.isalpha():
            message = ("Please enter letters only (a-z).", "yellow")

        elif len(guess) > 1:
            # Player tries to guess the whole word
            if guess == word:
                guessed.extend(list(word))
            else:
                mistakes += 1
                message = (f"'{guess}' is not the word!  (-1 life)", "red")

        elif guess in guessed or guess in wrong:
            message = (f"You already guessed '{guess}'. Try another letter.", "yellow")

        elif guess in word:
            guessed.append(guess)
            message = (f"Nice! '{guess}' appears {word.count(guess)} time(s).", "green")

        else:
            wrong.append(guess)
            mistakes += 1
            message = (f"Sorry, '{guess}' is not in the word.  (-1 life)", "red")

    # Round is over: show the final screen and a result banner
    if is_solved(word, guessed):
        render(word, category, guessed, wrong, mistakes, header, over="win")
        banner = [paint("★  YOU WIN!  ★", "bold", "green"),
                  f"The word was {paint(word.upper(), 'bold', 'cyan')}"]
        for line in box(banner, "green"):
            print("  " + line)
        return "win"

    render(word, category, guessed, wrong, mistakes, header, over="lose")
    banner = [paint("☠  GAME OVER  ☠", "bold", "red"),
              f"The word was {paint(word.upper(), 'bold', 'cyan')}"]
    for line in box(banner, "red"):
        print("  " + line)
    return "lose"


def ask_play_again():
    """Keep asking until the player answers y or n."""
    while True:
        answer = input("\n  " + paint("Play another round? (y/n): ", "cyan", "bold"))
        answer = answer.strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type 'y' or 'n'.")


def main():
    show_title()

    wins = 0
    losses = 0
    streak = 0
    best_streak = 0
    round_no = 1
    deck = []  # shuffled words, so no word repeats until all 5 are used

    while True:
        if not deck:
            deck = WORDS[:]
            random.shuffle(deck)
        word, category, clue = deck.pop()

        header = make_header(round_no, wins, losses, streak)
        result = play_round(word, category, clue, header)
        if result == "quit":
            break

        round_no += 1
        if result == "win":
            wins += 1
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            losses += 1
            streak = 0

        if not ask_play_again():
            break

    summary = [
        paint("FINAL SCORE", "bold", "yellow"),
        f"Wins {paint(str(wins), 'green', 'bold')}   "
        f"Losses {paint(str(losses), 'red', 'bold')}   "
        f"Best streak {paint(str(best_streak), 'yellow', 'bold')}",
        paint("Thanks for playing! Keep coding!", "cyan"),
    ]
    print()
    for line in box(summary, "magenta"):
        print("  " + line)
    print()


if __name__ == "__main__":
    main()
