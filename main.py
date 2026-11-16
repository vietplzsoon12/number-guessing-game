import random

import json
from pathlib import Path

# Difficulty settings: (maximum number, attempts)
DIFFICULTIES = {"1": ("Easy", 50, 10), "2": ("Medium", 100, 7), "3": ("Hard", 200, 5)}

# Store scores next to this Python file
SCORE_FILE = Path(__file__).with_name("scores.json")


def load_scores():
    """Load saved high scores, if they exist."""
    if SCORE_FILE.exists():
        try:
            with open(SCORE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Couldn't load scores. Starting fresh.")

    return {}


def save_scores(scores):
    """Save high scores to a JSON file."""
    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file, indent=4)


def choose_difficulty():
    """Ask the player to choose a difficulty."""
    print("\nChoose your difficulty:")
    print("1. Easy   (1-50, 10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard   (1-200, 5 attempts)")

    while True:
        choice = input("\nEnter 1, 2, or 3: ").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("Invalid choice! Try again.")


def get_guess(max_number):
    """Get a valid number from the player."""
    while True:
        user_input = input("Enter your guess: ").strip()

        try:
            guess = int(user_input)
        except ValueError:
            print("⚠️ Please enter a whole number!")
            continue

        if 1 <= guess <= max_number:
            return guess

        print(f"⚠️ Enter a number between 1 and {max_number}.")


def play_game(scores):
    """Run one complete guessing game."""
    name, max_number, max_attempts = choose_difficulty()

    secret_number = random.randint(1, max_number)
    attempts_left = max_attempts

    print(f"\n🎮 {name} Mode!")
    print(f"Guess a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts.\n")

    while attempts_left > 0:
        guess = get_guess(max_number)
        attempts_left -= 1

        if guess == secret_number:
            attempts_used = max_attempts - attempts_left

            print(f"\n🎉 YOU WIN! It took {attempts_used} guesses!")

            previous_best = scores.get(name)

            if previous_best is None or attempts_used < previous_best:
                scores[name] = attempts_used
                save_scores(scores)
                print("🏆 NEW HIGH SCORE!")
            else:
                print(f"Your best score is {previous_best} guesses.")

            return

        if guess < secret_number:
            print("📈 Too low!")
        else:
            print("📉 Too high!")

        print(f"Attempts left: {attempts_left}\n")

    print(f"\n💀 Game over! The number was {secret_number}.")


def show_scores(scores):
    """Display the player's best scores."""
    print("\n🏆 YOUR HIGH SCORES")

    for name in ("Easy", "Medium", "Hard"):
        best = scores.get(name)

        if best is None:
            print(f"{name}: Not played yet")
        else:
            print(f"{name}: {best} guesses")


def main():
    """Main menu and game loop."""
    scores = load_scores()

    print("================================")
    print("   🎮 NUMBER GUESSING GAME 🎮")
    print("================================")

    while True:
        print("\n1. Play Game")
        print("2. View High Scores")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            play_game(scores)
        elif choice == "2":
            show_scores(scores)
        elif choice == "3":
            print("\n👋 Thanks for playing!")
            break
        else:
            print("Invalid option! Please try again.")


if __name__ == "__main__":
    main()
