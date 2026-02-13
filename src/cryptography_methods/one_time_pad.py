"""One-Time Pad cipher — encrypt and decrypt using XOR with a random binary key."""

from time import sleep
from random import SystemRandom

from .utils import useful


class OneTimePad:
    """Encrypt and decrypt text using the One-Time Pad (XOR) method.

    Provides theoretically unbreakable encryption when the key is truly
    random, as long as the plaintext, and never reused.
    """

    def __init__(self):

        self.system_random = SystemRandom()

        self.choice = useful.choice(
            to_print=useful.color(text="\nWhat do you want to do with the One-time Pad cipher ?", style="bright"),
            choices_values={
                1: "Encrypt",
                2: "Decrypt",
                3: "Show documentation"})
        if self.choice == 1:
            print("Encrypted text :", useful.color(text=self.encrypt_one_time_pad(), color="red"))
        elif self.choice == 2:
            self.decrypt_one_time_pad()
        else:
            print("https://en.wikipedia.org/wiki/One-time_pad")

    def encrypt_one_time_pad(self, key=None, text=None):
        """Encrypt text by XOR-ing its binary form with a binary key."""

        iterator = 0
        encrypted_text = ""

        # Defining the key and the text to encrypt
        if not text:
            text = input(useful.color(text="Enter the text to encrypt :\n", style="bright", is_input=True))
        text = useful.to_binary(text=text)
        text_bytes = len(text)
        if not key:
            is_generated = useful.choice(to_print="Do you want to generate a key ?", choices_values={
                1: "Yes",
                2: "No"})
            if is_generated == 1:
                key = ""
                for i in range(0, text_bytes):
                    key += str(self.system_random.randint(0, 1))
                print("Key :", useful.color(text=key, color="red"))
                sleep(1)
            else:
                while True:
                    key = input(useful.color(text="Enter the key :\n", style="bright", is_input=True))
                    key = useful.to_binary(text=key)
                    if len(key) >= text_bytes:
                        break
                    print(f"Your key must contain as many bytes as your text ({text_bytes})")

        # Encrypting part
        for bit in text:
            new_bit = int(bit) + int(key[iterator])

            # Xor operation
            if int(new_bit) % 2 == 0:
                encrypted_text += "0"
            else:
                encrypted_text += "1"
            iterator += 1

        return encrypted_text

    def decrypt_one_time_pad(self):
        """Decrypt OTP-encrypted text by re-applying XOR with the same key."""

        text = input(useful.color(text="Enter the encrypted text :\n", style="bright", is_input=True))
        text = useful.to_binary(text=text)
        text_bytes = len(text)
        while True:
            key = input(useful.color(text="Enter the key :\n", style="bright", is_input=True))
            key = useful.to_binary(text=key)
            if len(key) >= text_bytes:
                break
            print(f"Your key must contain as many bytes as your text ({text_bytes})")

        # We'll encrypt the encrypted text with the key
        print("Decrypted text :", useful.color(text=self.encrypt_one_time_pad(key=key, text=text), color="red"))
