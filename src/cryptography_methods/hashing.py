"""Hashing — compute and brute-force reverse cryptographic hash digests."""

from time import time
from itertools import product
from hashlib import blake2b, md5, sha3_512, sha512, sha256
from string import ascii_lowercase, ascii_uppercase, ascii_letters, digits, printable

from .utils import useful


class Hash:
    """Hash text with multiple algorithms and attempt brute-force reversal.

    Supported algorithms: SHA-256, SHA-512, SHA3-512, MD5, BLAKE2b.
    Reversal supports both dictionary attacks and character-set brute-force.
    """

    def __init__(self):

        self.alphabets = [ascii_lowercase, ascii_uppercase, ascii_letters, digits, str(ascii_letters + digits),
                          printable]
        self.type_length = {512: ["SHA256"], 1024: ["SHA512", "SHA3512", "BLAKE"], 256: ["MD5"]}

        self.choice = useful.choice(
            to_print=useful.color(text="\nWhat do you want to do with the Hash cipher ?", style="bright"),
            choices_values={
                1: "Encrypt",
                2: "Decrypt",
                3: "Show documentation"})
        if self.choice == 1:
            self.encrypt_hash()
        elif self.choice == 2:
            self.decrypt_hash()
        else:
            print("https://en.wikipedia.org/wiki/Hash_function")

    def encrypt_hash(self, to_crypt=None):
        """Compute the hash digest of a given text using the selected algorithm."""

        if to_crypt:
            if to_crypt[0] == "SHA256":
                return sha256(str(to_crypt[1]).encode('utf-8')).hexdigest()
            elif to_crypt[0] == "SHA512":
                return sha512(str(to_crypt[1]).encode('utf-8')).hexdigest()
            elif to_crypt[0] == "SHA3512":
                return sha3_512(str(to_crypt[1]).encode('utf-8')).hexdigest()
            elif to_crypt[0] == "MD5":
                return md5(str(to_crypt[1]).encode('utf-8')).hexdigest()
            return blake2b(useful.to_binary(to_crypt[1]).encode()).hexdigest()

        # Asking the password and the type of hash to the user
        password_to_hash = input(useful.color(text="Enter the password to hash :\n", style="bright", is_input=True))
        type_hash = useful.choice(to_print=useful.color(text="What's the the hash type ?", style="bright"),
                                  choices_values={
                                      1: "SHA 256",
                                      2: "SHA 512",
                                      3: "SHA3 512",
                                      4: "MD5",
                                      5: "Blake"})

        # Hashing the passwords
        if type_hash == 1:
            hashed_password = sha256(str(password_to_hash).encode('utf-8')).hexdigest()
        elif type_hash == 2:
            hashed_password = sha512(str(password_to_hash).encode('utf-8')).hexdigest()
        elif type_hash == 3:
            hashed_password = sha3_512(str(password_to_hash).encode('utf-8')).hexdigest()
        elif type_hash == 4:
            hashed_password = md5(str(password_to_hash).encode('utf-8')).hexdigest()
        else:
            hashed_password = blake2b(useful.to_binary(password_to_hash).encode()).hexdigest()

        print("The hash of", useful.color(text=password_to_hash, color="red"), "is",
              useful.color(text=str(hashed_password), color="red"))

    def decrypt_hash(self):
        """Attempt to reverse a hash digest via dictionary or brute-force attack."""

        counter = 0

        # Collecting the hash
        encrypted = input(useful.color(text="Enter the hash :\n", style="bright", is_input=True))
        while len(useful.to_binary(encrypted)) not in self.type_length.keys() and len(
                useful.to_binary(encrypted)) - 1 not in self.type_length.keys() and len(
            useful.to_binary(encrypted)) + 1 not in self.type_length.keys():
            print("Please enter a valid hash")
            encrypted = input(useful.color(text="Enter the hash :\n", style="bright", is_input=True))

        # Rapproaching it of a type of hash method
        encrypted_types = ""
        for length in self.type_length.keys():
            if len(useful.to_binary(encrypted)) - length in [-1, 0, 1]:
                encrypted_types = self.type_length[length]

        # Is the user using a dictionnary
        if_dictionnary = useful.choice(useful.color(text="Do you want to use a dictionnary ?", style="bright"),
                                       choices_values={
                                           1: "Yes",
                                           2: "No"})
        if if_dictionnary == 1:
            while True:
                try:
                    with open(input(
                            useful.color(text="Enter the file (Exemple : C:/User/Document/Dict.txt)\n",
                                         style="bright", is_input=True)).replace("/", "\\"), "r") as my_dict:

                        begin_time = time()
                        possibilities = my_dict.read().split("\n")
                        for password in possibilities:

                            # Inform the user of the advancement
                            if counter % 100000 == 0 and counter != 0:
                                print("*", useful.color(text=str(
                                    '{:,}'.format(counter).replace(',', ' ')) + "tries has been done",
                                                        color="green"), "*")

                            # Watch if the hash matches
                            for encrypted_type in encrypted_types:
                                if self.encrypt_hash(to_crypt=[encrypted_type, password]) == encrypted:
                                    print("\n\n\n\t\t\t\tPassword found :", useful.color(text=password,
                                                                                         color="red"))
                                    print("\n\n\tFounded in",
                                          useful.color(text=str((time() - begin_time).__round__(5)), color="red"),
                                          "seconds and",
                                          useful.color(text=str('{:,}'.format(counter).replace(',', ' ')),
                                                       color="red"), "tries")
                                    return

                            counter += 1
                            continue
                        print("The password isn't in the dictionnary")
                        return
                except FileNotFoundError:
                    print("The file isn't valid")

        alphabet_choice = useful.choice(
            useful.color(text="With which characters do you want to decrypt ?", style="bright"),
            choices_values={1: "alpha lowercase",
                            2: "alpha uppercase",
                            3: "alpha",
                            4: "digits",
                            5: "alpha and digits",
                            6: "alpha, digits and other chars"})
        alphabet_used = self.alphabets[alphabet_choice - 1]
        s_begin_time = time()

        for i in range(1, 10):

            # Generating possible passwords according to used alphabet
            possibilities = product(alphabet_used, repeat=i)
            for password in possibilities:
                word = ""
                count = 0
                while count < i:
                    word += password[count]
                    count += 1

                # Warn the user about the length of the process
                if counter == len(alphabet_used) ** i:
                    if i >= 5:
                        user_choice = useful.choice(
                            to_print=f"Do you want to continue ? (Test all the {i} characters passwords "
                                     f"could take time)",
                            choices_values={
                                1: "Yes",
                                2: "No(quit)"})
                        if user_choice == 2:
                            return
                    print("\n\t\t\t\tAll", useful.color(text=str(i), color="red"),
                          "character passwords have been tested\n")

                # Inform the user of the advancement
                if counter % 100000 == 0 and counter != 0:
                    print("*", useful.color(text=str('{:,}'.format(counter).replace(',', ' ')) +
                                                 " tests have been carried out", color="green"), "*")

                # Watch if the hash matches
                for encrypted_type in encrypted_types:
                    if self.encrypt_hash(to_crypt=[encrypted_type, word]) == encrypted:
                        print("\n\n\n\t\t\t\tPassword found :", useful.color(text=word, color="red"))
                        print("\n\n\tFounded in",
                              useful.color(text=str((time() - s_begin_time).__round__(5)), color="red"),
                              "seconds and",
                              useful.color(text=str('{:,}'.format(counter).replace(',', ' ')), color="red"),
                              "tries")
                        return
                counter += 1
