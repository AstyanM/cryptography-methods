"""RSA cipher — asymmetric encryption with prime-number key generation."""

from random import SystemRandom
from time import time

from .utils import useful


class RSA:
    """Encrypt and decrypt messages using the RSA public-key cryptosystem.

    Includes Miller-Rabin primality testing for key generation,
    the extended Euclidean algorithm, and modular exponentiation.
    """

    def __init__(self):

        self.system_random = SystemRandom()

        self.choice = useful.choice(
            to_print=useful.color(text="\nWhat do you want to do with the RSA cipher ?", style="bright"),
            choices_values={
                1: "Encrypt",
                2: "Decrypt",
                3: "Show documentation"})
        if self.choice == 1:
            self.encrypt_rsa()
        elif self.choice == 2:
            self.decrypt_rsa()
        else:
            print("https://en.wikipedia.org/wiki/RSA_cipher")

    def witness_test(self, number, aleatory):
        """Return whether *aleatory* is a Miller-Rabin witness for the compositeness of *number*."""

        new_number = number - 1
        exponent = 0

        while new_number % 2 == 0:
            exponent += 1
            new_number //= 2
        multiplier = new_number
        integer = pow(aleatory, multiplier, number)
        if integer in (1, number - 1):
            return False
        for i in range(0, exponent - 1):
            integer = integer ** 2 % number
            if integer == number - 1:
                return False
        return True

    def miller_rabin(self, number):
        """Find a probable prime >= *number* using the Miller-Rabin primality test."""

        k = 28
        f_time = time()
        my_number = number

        while True:
            for i in range(0, k):
                aleatory = self.system_random.randint(2, my_number - 2)
                if not self.witness_test(my_number, aleatory):
                    print(useful.color(text=my_number, color="red"))
                    print("Generated in", useful.color(text=str((time() - f_time).__round__(5)), color="red"),
                          "seconds")
                    return my_number
                if int(str(my_number)[-1]) + 2 == 5:
                    my_number += 4
                else:
                    my_number += 2

    def create_prime_numbers(self, num_bits):
        """Generate a random probable prime of *num_bits* bits."""

        bin_num = ""

        for i in range(0, num_bits - 1):
            bin_num += str(self.system_random.randint(0, 1))
        bin_num += "1"
        num = int(bin_num, 2)
        prime_number = self.miller_rabin(number=num)

        return prime_number

    def euclide(self, f_int, s_int):
        """Compute gcd(*f_int*, *s_int*) using the Euclidean algorithm."""

        rest = f_int - s_int * (f_int // s_int)

        while rest != 0:
            new_int = s_int
            s_int = rest
            rest = new_int - s_int * (new_int // s_int)

        return s_int

    def calculate_e(self, phi):
        """Choose a random integer *e* coprime with *phi* (Euler's totient)."""

        min_range = 1
        e_num = self.system_random.randint(min_range, phi)

        while self.euclide(phi, e_num) != 1:
            e_num = self.system_random.randint(min_range, phi)

        return e_num

    def euclide_extended(self, f_num, s_num):
        """Compute the extended Euclidean algorithm, returning (gcd, x, y)."""

        rest, f_int, s_int, new_rest, new_f_int, new_s_int = f_num, 1, 0, s_num, 0, 1

        while new_rest != 0:
            quotient = rest // new_rest
            rest, f_int, s_int, new_rest, new_f_int, new_s_int = new_rest, new_f_int, new_s_int, rest - quotient * \
                                                                 new_rest, f_int - quotient * new_f_int, s_int - \
                                                                 quotient * new_s_int

        return rest, f_int, s_int

    def encrypt_rsa(self):
        """Encrypt a numeric message using an RSA public key (n, e)."""

        # Defining the differents levels of security
        min_secure = 512
        mid_secure = 768
        max_secure = 1024

        key_choice = useful.choice(
            to_print=useful.color(text="Do you want to create a public and private key ?", style="bright"),
            choices_values={
                1: "Yes",
                2: "No"})

        # If the user already have a public key
        if key_choice == 1:
            chosen_secure = useful.choice(
                to_print=useful.color(text="What's the length (in bits) of the prime factors :",
                                      style="bright"),
                choices_values={1: "min security (512)",
                                2: "mid security (768)",
                                3: "max security (1024)",
                                4: "personalized"})

            if chosen_secure == 1:
                bit_len = min_secure
            elif chosen_secure == 2:
                bit_len = mid_secure
            elif chosen_secure == 3:
                bit_len = max_secure
            else:
                while True:
                    try:
                        bit_len = abs(int(input("Enter the length : ")))
                        if bit_len <= 1:
                            print("Please enter a valid integer")
                        else:
                            break
                    except ValueError:
                        print("Please enter a valid choice")

            # Generating all the required numbers
            print("\np = ", end="")
            p_int = self.create_prime_numbers(bit_len)
            print("\nq = ", end="")
            q_int = self.create_prime_numbers(bit_len)
            n_int = p_int * q_int
            phi = (p_int - 1) * (q_int - 1)
            e_int = self.calculate_e(phi=phi)
            d_int = self.euclide_extended(f_num=e_int, s_num=phi)[1]

            print("\nYou public key :", useful.color(text=(n_int, e_int), color="red"))
            print("Your private key :", useful.color(text=(n_int, d_int), color="red"))

        else:
            to_print = {"n": "n (result of p*q)", "e": "e (prime with (p-1)*(q-1))"}
            n_e = []
            for key in "ne":
                while True:
                    try:
                        key_value = int(
                            input("Enter the value of " + useful.color(text=to_print[key], color="red") + " : "))
                        n_e.append(key_value)
                        break
                    except ValueError:
                        print("Please enter a valid value")
            n_int = n_e[0]
            e_int = n_e[1]

        # Collecting the message to encrypt
        while True:
            user_mess = input("Enter the message to encrypt with form (num1 num2 ... numx): ").split(" ")
            try:
                mess = [int(mess) for mess in user_mess]
                break
            except ValueError:
                print("Please enter a valid message")

        encrypted_mess = [pow(mess_part, e_int, n_int) for mess_part in mess]

        print("Encrypted message :", end=" ")
        print(" ".join([useful.color(text=str(encrypted_part), color="red") for encrypted_part in encrypted_mess]))

    def decrypt_rsa(self):
        """Decrypt an RSA-encrypted numeric message using the private key (n, d)."""

        n_int = int(input("\nEnter value of " + useful.color(text="n", color="red") + " : "))
        d_int = int(input("Enter value of " + useful.color(text="d", color="red") + " : "))

        while True:
            user_mess = input("Enter the message to decrypt with form (num1 num2 ... numx): ").split(" ")
            try:
                encrypted_mess = [int(mess) for mess in user_mess]
                break
            except ValueError:
                print("Please enter a valid message")
        decrypted_mess = [pow(int(mess_part), d_int, n_int) for mess_part in encrypted_mess]

        print("Decrypted message :", end=" ")
        print(" ".join([useful.color(text=str(decrypted_part), color="red") for decrypted_part in decrypted_mess]))
