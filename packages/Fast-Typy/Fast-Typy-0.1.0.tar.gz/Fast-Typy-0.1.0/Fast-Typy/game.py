"""
The Game class that contains the code for the game.

:Author: Prince Carl Velasco
:Date: 2022-06-12
:Version: 0.1.0
:Description:
    - It contains the main menu.
    - It contains the game start function.
    - It contains the high score function.
    - It contains the add words function.
    - It contains the list of words function.
:Example:
    $ python main.py

    [1] Game Start
    [2] High Score
    [3] Add Words
    [4] List of Words
    Input: 1

    The timer will start in 5...
    4...
    3...
    2...
    1...
    Timer started!

    Easy
    1st word: Dog
    your input: dgo
    Try again!
"""
import csv
import random
import time
from pathlib import Path

from constants import EASY_WORDS
from constants import EASY_WORDS_FILE
from constants import HARD_WORDS
from constants import HARD_WORDS_FILE
from constants import HIGH_SCORE_FILE
from constants import INTERMEDIATE_WORDS
from constants import INTERMEDIATE_WORDS_FILE
from utils import nth


class Game:
    def __init__(self):
        self.words = []
        self.high_scores = {}
        self.easy_words = []
        self.intermediate_words = []
        self.hard_words = []

    def start(self):
        self.load_words()
        self.load_high_scores()
        self.menu()
        self.end()

    def end(self):
        self.export_words()
        self.export_high_scores()

    def menu(self):
        print("""[1] Game Start
[2] High Score
[3] Add Words
[4] List of Words""")
        choice = int(input("Input: "))

        switch = {
            1: self.game_start,
            2: self.high_score,
            3: self.add_words,
            4: self.list_of_words
        }
        switch[choice]()

    def game_start(self):
        """
        This function starts the game.

        :return: None
        """

        print("[1] Game Start")
        print("The timer will start in 5...")
        for i in range(4):
            print(f"{4 - i}...")
        print("Timer started!\n")
        start = time.time()

        easy_words = random.sample(self.easy_words, 3)
        intermediate_words = random.sample(self.intermediate_words, 4)
        hard_words = random.sample(self.hard_words, 3)

        counter = 1
        word_list = easy_words + intermediate_words + hard_words
        for i in range(len(word_list)):
            if i == 0:
                print("Easy")
            elif i == 3:
                print("Intermediate")
            elif i == 7:
                print("Hard")

            word = word_list[i].replace("\n", "")
            print(f"{nth(counter)} word: {word}")

            guess = input("your input: ")
            while guess != word:
                print("Try again!")
                print()

                print(f"{nth(counter)} word: {word}")
                guess = input("your input: ")

            counter += 1
            print("Correct!")
            print()

        end = time.time()
        duration = int(end - start)
        print(f"It took you {duration} seconds to enter the {len(word_list)} words correctly!")

        print("Enter your name so I can put you into our record books.")
        name = input("Your name: ")
        self.high_scores[len(self.high_scores) + 1] = [name, f"{duration}s"]

        print()

    def high_score(self):
        print()

        header = ["rank", "name", "time"]
        print("High Scores\n")
        print(f"{header[0]:<10} {header[1]:<14} {header[2]}")

        for rank, value in self.high_scores.items():
            try:
                print(f"{rank:<10} {value[0]:<14} {value[1]}")
            except IndexError:
                print("---- No high scores yet ----")

        print()

    def add_words(self):
        print()

        print("[3] Add Words")
        print("Enter new word")
        word = input("Input: ")
        word_length = len(word)

        if word_length <= 5:
            self.easy_words.append(word)
            print(f"{word} added to the easy list")
        elif 6 <= word_length <= 8:
            self.intermediate_words.append(word)
            print(f"{word} added to the intermediate list")
        else:
            self.hard_words.append(word)
            print(f"{word} added to the hard list")

        print()

    def list_of_words(self):
        print()

        print("""[4] List of Words
        [1] View easy words
        [2] View intermediate words
        [3] View hard words""")
        choice = int(input("Input: "))

        if choice == 1:
            for word in self.easy_words:
                print(word)
            print(f"There are {len(self.easy_words)} words in the \"easy\" list")
        elif choice == 2:
            for word in self.intermediate_words:
                print(word)
            print(f"There are {len(self.intermediate_words)} words in the \"intermediate\" list")
        elif choice == 3:
            for word in self.hard_words:
                print(word)
            print(f"There are {len(self.hard_words)} words in the \"hard\" list")

    def load_words(self):
        if Path(EASY_WORDS_FILE).exists():
            with open(EASY_WORDS_FILE, "r", encoding="UTF8") as f:
                for line in f:
                    self.easy_words.append(line.replace("\n", ""))
        else:
            for word in EASY_WORDS:
                self.easy_words.append(word)

        if Path(INTERMEDIATE_WORDS_FILE).exists():
            with open(INTERMEDIATE_WORDS_FILE, "r", encoding="UTF8") as f:
                for line in f:
                    self.intermediate_words.append(line.replace("\n", ""))
        else:
            for word in INTERMEDIATE_WORDS:
                self.intermediate_words.append(word)

        if Path(HARD_WORDS_FILE).exists():
            with open(HARD_WORDS_FILE, "r", encoding="UTF8") as f:
                for line in f:
                    self.hard_words.append(line.replace("\n", ""))
        else:
            for word in HARD_WORDS:
                self.hard_words.append(word)

    def export_words(self):
        with open(EASY_WORDS_FILE, "w+", encoding="UTF8") as f:
            for word in self.easy_words:
                print(word, sep="\n", file=f)
        with open(INTERMEDIATE_WORDS_FILE, "w+", encoding="UTF8") as f:
            for word in self.intermediate_words:
                print(word, sep="\n", file=f)
        with open(HARD_WORDS_FILE, "w+", encoding="UTF8") as f:
            for word in self.hard_words:
                print(word, sep="\n", file=f)

    def load_high_scores(self):
        file = Path(HIGH_SCORE_FILE)

        if file.exists():
            with open(HIGH_SCORE_FILE, "r", encoding="UTF8") as f:
                lines = f.readlines()
                for line in lines[1:]:
                    score = line.strip().split(",")
                    try:
                        self.high_scores[int(score[0])] = [score[1], score[2]]
                    except IndexError:
                        pass
        else:
            file.touch()

    def export_high_scores(self):
        sorted_high_scores = {
            k: v for k, v in sorted(self.high_scores.items(), key=lambda item: int(item[1][1][:-1]))
        }

        with open(HIGH_SCORE_FILE, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "name", "time"])

            for rank, (name, duration) in zip(range(1, len(sorted_high_scores) + 1), sorted_high_scores.values()):
                writer.writerow([rank, name, duration])
