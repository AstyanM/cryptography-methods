"""Vigenere cipher — polyalphabetic substitution using a repeating keyword."""

from .utils import useful


class Vigenere:
    """Encrypt and decrypt text using the Vigenere polyalphabetic cipher.

    Uses a repeating keyword to shift each character by a varying amount,
    making simple frequency analysis ineffective.
    """

    def __init__(self):

        self.choice = useful.choice(
            to_print=useful.color(text="\nWhat do you want to do with the Vigenere cipher ?", style="bright"),
            choices_values={
                1: "Encrypt",
                2: "Decrypt",
                3: "Show documentation"})
        if self.choice == 1:
            self.encrypt_vigenere()
        elif self.choice == 2:
            self.decrypt_vigenere()
        else:
            print("https://en.wikipedia.org/wiki/Vigenere_ciphers")

    def encrypt_vigenere(self):
        """Encrypt text by adding letter positions of the plaintext and keyword."""

        text = ""
        key = ""
        iterator = 0
        encrypted_text = ""

        # Defining the key and the text to encrypt
        input_text = input(useful.color(text="Enter the text to encrypt :\n", style="bright", is_input=True)).lower()
        for char in input_text:
            text += useful.become_alpha(letter=char)
        input_key = input(useful.color(text="Enter the key :\n", style="bright", is_input=True)).lower()
        for char in input_key:
            key += useful.become_alpha(letter=char)

        # Encrypt the text
        for clear_char in text:
            # We add the position of the text's character to the position of the key's character
            encrypted_text += useful.alpha[(useful.alpha.index(clear_char) + useful.alpha.index(
                key[iterator % len(key)])) % 26]
            iterator += 1

        print("Encrypted text :", useful.color(text=encrypted_text, color="red"))

    def decrypt_vigenere(self):
        """Decrypt Vigenere-encrypted text by subtracting the keyword positions."""

        text = ""
        key = ""
        iterator = 0
        decrypted_text = ""

        # Asking the user for all the informations
        encrypted_text = input(useful.color(text="Enter the text to decrypt :\n", style="bright", is_input=True))
        for char in encrypted_text:
            text += useful.become_alpha(letter=char)
        input_key = input(useful.color(text="Enter the key :\n", style="bright", is_input=True))
        for char in input_key:
            key += useful.become_alpha(letter=char)

        # Start to decrypt
        for char in encrypted_text:
            decrypted_text += useful.alpha[
                (useful.alpha.index(char) - useful.alpha.index(key[iterator % len(key)])) % 26]
            iterator += 1

        print("Decrypted text :", useful.color(text=decrypted_text, color="red"))
