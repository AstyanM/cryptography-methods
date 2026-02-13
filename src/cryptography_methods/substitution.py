"""Substitution cipher — encrypt and decrypt using a letter-for-letter mapping."""

from copy import deepcopy
from time import time

from .utils import useful


class Substitution:
    """Encrypt and decrypt text using a mono-alphabetic substitution cipher.

    Supports manual key entry for encryption and pattern-based dictionary
    attack for decryption without a key.
    """

    def __init__(self):

        self.choice = useful.choice(
            to_print=useful.color(text="\nWhat do you want to do with the Substitution cipher ?", style="bright"),
            choices_values={
                1: "Encrypt",
                2: "Decrypt",
                3: "Show documentation"})
        if self.choice == 1:
            print("Encrypted text :", useful.color(text=self.encrypt_substitution(), color="red"))
        elif self.choice == 2:
            self.decrypt_substitution()
        else:
            print("https://en.wikipedia.org/wiki/Substitution_cipher")

    def pattern(self, word):
        """Compute the letter-repetition pattern of a word for dictionary matching."""

        substitute = Substitution()

        dico = {}
        letters = []
        for letter in word:
            letter = useful.become_alpha(letter)
            letters.append(letter)
        i = 0
        used_chars = []
        for char in letters:
            if char not in used_chars:
                used_chars.append(char)
                dico[char] = useful.alpha[i]
                i += 1

        new_words = substitute.encrypt_substitution(text=word, dico=dico)

        return new_words

    def create_dictionnary(self, word1, word2):
        """Build a substitution mapping between two words of equal length."""

        dico = {}

        if isinstance(word1, list):
            word1 = "".join(word1)
        if isinstance(word2, list):
            word2 = "".join(word2)

        for letter in word1.lower():
            if letter not in dico.items() and letter != " ":
                dico[word2[word1.index(letter)]] = letter

    def encrypt_substitution(self, text=None, dico=None):
        """Encrypt text by substituting each letter according to the given mapping."""

        my_alpha = deepcopy(useful.alpha)
        encrypted_text = ""
        new_alpha = {}
        used_letters = 0

        # If the user have to fill some informations
        if not text:
            text = input(useful.color(text="Enter the text to encrypt :\n", style="bright", is_input=True))
        if not dico:
            while used_letters < 26:
                if used_letters == 25:
                    new_alpha[useful.alpha[used_letters]] = my_alpha[0]
                    break
                input_char = useful.choice(
                    to_print="Chars you have to use : " + useful.color(text=my_alpha, color="red") +
                             f"\nEnter the letter to substitute to {useful.alpha[used_letters]} : ",
                    list_possible_values=my_alpha)
                new_alpha[useful.alpha[used_letters]] = input_char
                my_alpha.remove(new_alpha[useful.alpha[used_letters]])
                used_letters += 1
        else:
            new_alpha = dico

        # Substitute each character according to the dictionnary
        for other_char in text.lower():
            if other_char in useful.alpha_bis:
                encrypted_text += new_alpha[useful.alpha_bis[other_char]]
            elif other_char in useful.alpha:
                encrypted_text += new_alpha[other_char]
            else:
                encrypted_text += other_char

        return encrypted_text

    def decrypt_substitution(self):
        """Decrypt substitution-encrypted text using a known key or pattern-based attack."""

        # Defining the text to decrypt
        text = input(useful.color(text="Enter the text to decrypt :\n", style="bright", is_input=True)).lower()

        # If the user know the dictionnary
        user_choice = useful.choice(to_print=useful.color(text="Do you know the dictionnary ?", style="bright"),
                                    choices_values={
                                        1: "Yes",
                                        2: "No"})
        if user_choice == 1:
            print("Decrypted text :", useful.color(text=self.encrypt_substitution(text=text), color="red"))

        else:
            # Choosing the language
            language_choosed = useful.choice(
                to_print=useful.color(text="In which language has it been encrypted ?", style="bright"),
                choices_values=useful.language_choices)
            begin_time = time()
            if language_choosed == 3:
                language_choosed = [1, 2]
            else:
                language_choosed = [language_choosed]

            for language_choosen in language_choosed:
                print("Language :", useful.color(text=useful.language_choices[language_choosen], style="bright"),
                      end="\n\n")

                with open(useful.languages[useful.language_choices[language_choosen]], "r") as words:

                    all_words = sorted(words.read().split("\n"), key=len)
                    all_words_len = {}
                    all_unfound_words = []

                    # Creating a dict sorted by length
                    for iterator in range(1, len(all_words[-1])):
                        all_words_len[iterator] = []
                        [all_words_len[iterator].append(word) for word in all_words if len(word) == iterator]

                    # Creating an usable text
                    encrypted_text = ""
                    for char in text:
                        if char not in useful.alpha and char not in useful.alpha_bis and char != 0:
                            encrypted_text += " "
                        else:
                            encrypted_text += char
                    encrypted_text = encrypted_text.split(" ")
                    encrypted_text = [encrypted_word.strip() for encrypted_word in encrypted_text]

                    # Creating a list with all the used words
                    used_words = []
                    already_used_pos = {}
                    iterator = 0
                    for encrypted_word in encrypted_text:
                        if encrypted_word not in used_words:
                            used_words.append(encrypted_word)
                        elif encrypted_text.index(encrypted_word) not in already_used_pos:
                            already_used_pos[iterator] = encrypted_text.index(encrypted_word)
                        iterator += 1

                    # Starting to decrypt the text
                    pos_sentences = []
                    len_crypted_text = len(encrypted_text)
                    num_unvalid_word = 0
                    i = 0

                    while i < len_crypted_text - num_unvalid_word:

                        new_pos_sentences = []
                        encrypted_word = encrypted_text[i]
                        len_crypted_word = len(encrypted_word)

                        # Made to decrypt faster the first word
                        if i == 0:
                            for word in all_words_len[len_crypted_word]:
                                if self.pattern(word) == self.pattern(encrypted_word):
                                    new_pos_sentences.append(word)

                        # Each possible word is added to each possible sentence and watching if the pattern is valid
                        else:
                            for pos_sentence in pos_sentences:
                                if i in already_used_pos.keys():
                                    new_pos_sentences.append(
                                        " ".join([pos_sentence, pos_sentence.split(" ")[already_used_pos[i]]]))
                                else:
                                    for other_word in all_words_len[len_crypted_word]:
                                        if self.pattern(" ".join([pos_sentence, other_word])) == self.pattern(
                                                " ".join(encrypted_text[: i + 1])):
                                            new_pos_sentences.append(" ".join([pos_sentence, other_word]))

                        # If there's no possibilities
                        if not new_pos_sentences:
                            all_unfound_words.append(encrypted_text[i])
                            encrypted_text.remove(encrypted_text[i])
                            num_unvalid_word += 1

                        # Else, adding the new possibilities
                        else:
                            pos_sentences = deepcopy(new_pos_sentences)
                            print("All the possible sentences for the moment :",
                                  useful.color(text=pos_sentences, color="red"))
                            i += 1
                    if all_unfound_words:
                        print("\nSome word have not been found :",
                              useful.color(text=" / ".join(all_unfound_words), color="red"))
                        print("This can be due to a bad dictionnary")
                    print(useful.color(text="\nPossible sentences :", style="bright"))
                    my_text = " ".join(encrypted_text)
                    [print(useful.color(text=sentence, color="red"), "with dict :",
                           useful.color(text=self.create_dictionnary(sentence, my_text), color="red")) for sentence
                     in pos_sentences]
                    print("\nFound in", useful.color(text=str((begin_time - time().__round__(5))), color="red"),
                          "seconds")
