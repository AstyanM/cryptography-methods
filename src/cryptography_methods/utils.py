"""Shared utilities for text processing, user interaction, and terminal output."""

from pathlib import Path
from string import ascii_lowercase
from functools import reduce

from colorama import init, Fore, Style

_DATA_DIR = Path(__file__).resolve().parent / "data"


class Useful:
    """Utility class providing helpers for alphabet handling, user I/O, and text formatting."""

    def __init__(self):

        init()

        self.alpha = list(ascii_lowercase)
        self.alpha_bis = {"à": "a", "â": "a", "ä": "a", "é": "e", "è": "e", "ê": "e", "ù": "u", "ü": "u", "î": "i",
                          "ï": "i", "ç": "c", "ô": "o", "œ": "oe"}  # Letters that become without accent
        self.languages = {"French": str(_DATA_DIR / "french_dict.txt"),
                          "English": str(_DATA_DIR / "english_dict.txt")}
        self.language_choices = {1: "French", 2: "English", 3: "Don't know"}

    def choice(self, to_print, choices_values=None, list_possible_values=None):
        """Prompt the user to make a valid choice from a numbered menu or a list of values."""

        if choices_values:
            print(to_print)
            choices_values = dict(choices_values)
            while True:
                for choice in choices_values.keys():
                    print(f"{str(choice)} : {str(choices_values[choice])}")
                user_choice = input("")
                if str(user_choice) in str(choices_values.keys()) and str(user_choice) != "":
                    return int(user_choice)
                print("\nPlease enter a valid choice : ")

        if list_possible_values:
            print(to_print, end="")
            while True:
                user_choice = input("")
                if str(user_choice) in str(list_possible_values) and str(user_choice) != "":
                    return user_choice
                print("\nPlease enter a valid choice : ", end="")

    def see_if_language(self, encrypted_sentences, language=None):
        """Check if decrypted text candidates match words from the specified language dictionary."""

        with open(self.languages[language], "r") as words:

            all_words = words.read().split("\n")
            possibilities = []
            for encrypted_sentence in encrypted_sentences:
                encrypted_words = encrypted_sentence[0].split(" ")
                counter = 0
                for encrypted_word in encrypted_words:
                    if encrypted_word.lower() in all_words and encrypted_word.lower() != "":
                        counter += 1
                if len(encrypted_words) <= 2:
                    if counter >= 1:
                        possibilities.append(encrypted_sentence)
                elif 2 < len(encrypted_words) <= 5:
                    if counter >= 2:
                        possibilities.append(encrypted_sentence)
                elif 5 < len(encrypted_words) <= 10:
                    if counter >= 3:
                        possibilities.append(encrypted_sentence)
                elif 10 < len(encrypted_words) <= 20:
                    if counter >= 5:
                        possibilities.append(encrypted_sentence)
                else:
                    if counter >= 7:
                        possibilities.append(encrypted_sentence[1])

            return possibilities

    def become_alpha(self, letter):
        """Normalize a character to its lowercase ASCII equivalent, stripping accents."""

        letter = str(letter).lower()

        if letter in self.alpha_bis:
            return self.alpha_bis[letter]
        elif letter in self.alpha:
            return letter
        return ""

    def to_binary(self, text):
        """Convert a text string to its binary representation."""

        for char in text:
            if char not in ["0", '1']:
                text = bin(reduce(lambda x, y: 256 * x + y, (ord(char) for char in text), 0)).replace("b", "")
                break
        return text

    def color(self, text, color="white", style="normal", is_input=False):
        """Apply terminal color and style formatting to text using colorama."""

        color_map = {
            "black": Fore.BLACK,
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
        }

        style_map = {
            "dim": Style.DIM,
            "normal": Style.NORMAL,
            "bright": Style.BRIGHT,
        }

        if is_input:
            print(color_map[color] + style_map[style] + str(text) + Style.RESET_ALL, end="")
            return ""
        return color_map[color] + style_map[style] + str(text) + Style.RESET_ALL


useful = Useful()
