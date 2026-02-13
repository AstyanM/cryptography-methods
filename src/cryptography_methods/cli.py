"""Interactive command-line interface for selecting and running cipher modules."""

from time import sleep
from sys import exit as sys_exit

from .utils import useful
from .caesar import Caesar
from .transposition import Transposition
from .substitution import Substitution
from .vigenere import Vigenere
from .one_time_pad import OneTimePad
from .hashing import Hash
from .rsa import RSA


def main():
    """Launch the interactive menu for choosing a cryptographic method."""

    while True:
        user_choice = useful.choice(
            to_print=useful.color(text="\nWhich encryption method do you want to use ?", style="bright"),
            choices_values={
                1: "Caesar",
                2: "Transposition",
                3: "Substitution",
                4: "Vigenere",
                5: "One-time Pad",
                6: "Hash",
                7: "RSA",
                8: "Credits",
                9: "Exit"})
        if user_choice == 1:
            Caesar()
        elif user_choice == 2:
            Transposition()
        elif user_choice == 3:
            Substitution()
        elif user_choice == 4:
            Vigenere()
        elif user_choice == 5:
            OneTimePad()
        elif user_choice == 6:
            Hash()
        elif user_choice == 7:
            RSA()
        elif user_choice == 8:
            print("\n\t\t\t", useful.color(text="Sources :", color="red"),
                  "\n-", useful.color(text="\"Histoire des Codes Secrets\"", color="green"), "from",
                  useful.color(text="Simon Singh", style="bright"),
                  "\n-", useful.color(text="\"La Science des Codes Secrets\"", color="green"), "from",
                    useful.color(text="Les mystères de la science", style="bright"),
                  "\n- http://inventwithpython.com/cracking/chapter7.html, a chapter that helps me "
                  "to decrypt the transposition cipher"
                  "\n- https://www.drgoulu.com/2012/04/15/comment-produire-des-nombres-premiers/, a website that "
                  "taught me how to generate large prime numbers"
                  "\n\n\t\t\t", useful.color(text="Thanks :", color="red"),
                    "\n", useful.color(text=".H.D.1.", color="green"),
                  "from the OpenClassrooms forum who helped me to solve an Overflow type error"
                  "\n", useful.color(text="Oznérol", color="green"),
                  "from the JACHAMPAGNE Discord who helped me to compile my program"
                  "\n\n\t\t\t", useful.color(text="Author :", color="red"),
                  "\n", useful.color(text="MARTIN Astyan", color="green"))
        else:
            sleep(1)
            print(useful.color(text="\nGoodbye", color="green"))
            sleep(1.5)
            sys_exit()

        if user_choice != 9:
            input()
            if_exit = useful.choice(to_print=useful.color(text="\nDo you want to quit the program ?", style="bright",
                                                          is_input=True), choices_values={
                                                                                    1: "Yes",
                                                                                    2: "No"})
            if if_exit == 1:
                sleep(1)
                print(useful.color(text="\nGoodbye", color="green"))
                sleep(1.5)
                sys_exit()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("")
        print("\n! Program interrupted !")
