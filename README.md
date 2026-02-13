# Cryptography Methods

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Ciphers](https://img.shields.io/badge/Ciphers-7%20methods-orange)

An interactive command-line toolkit implementing **seven classical and modern cryptographic algorithms** from scratch. Built as an educational project to explore the mathematics and logic behind encryption — from ancient shift ciphers to RSA public-key cryptography.

## Motivation

This project was inspired by Simon Singh's _"The Code Book"_ and aims to provide hands-on understanding of how cryptographic methods work under the hood. Each algorithm is implemented without relying on high-level crypto libraries (except Python's `hashlib` for hashing), making the underlying mechanics transparent and easy to study.

## Features

| Cipher                                              | Encrypt | Decrypt (with key) |         Decrypt (brute-force)         |
| --------------------------------------------------- | :-----: | :----------------: | :-----------------------------------: |
| **Caesar**                                          |   Yes   |        Yes         | Yes — shift enumeration + dictionary  |
| **Transposition**                                   |   Yes   |        Yes         |  Yes — key enumeration + dictionary   |
| **Substitution**                                    |   Yes   |        Yes         | Yes — pattern-based dictionary attack |
| **Vigenere**                                        |   Yes   |        Yes         |                   —                   |
| **One-Time Pad (XOR)**                              |   Yes   |        Yes         |                   —                   |
| **Hash** (SHA-256, SHA-512, SHA3-512, MD5, BLAKE2b) |   Yes   |         —          |    Yes — dictionary + brute-force     |
| **RSA**                                             |   Yes   |        Yes         |                   —                   |

### Highlights

- **Dictionary-aided decryption** — French and English word lists are used to automatically identify plausible plaintext candidates during brute-force attacks.
- **RSA key generation** — Includes Miller-Rabin primality testing and the extended Euclidean algorithm for generating large prime-based key pairs (512–1024 bit factors).
- **Colorized terminal UI** — Interactive menu with colored output for readability.

## Architecture

```
cryptography-methods/
├── src/
│   └── cryptography_methods/
│       ├── __init__.py          # Package exports
│       ├── __main__.py          # python -m entry point
│       ├── cli.py               # Interactive menu
│       ├── utils.py             # Shared utilities (alphabet, I/O, colors)
│       ├── caesar.py            # Caesar (shift) cipher
│       ├── transposition.py     # Columnar transposition cipher
│       ├── substitution.py      # Mono-alphabetic substitution cipher
│       ├── vigenere.py          # Vigenere polyalphabetic cipher
│       ├── one_time_pad.py      # One-Time Pad (XOR) cipher
│       ├── hashing.py           # Hash functions + brute-force reversal
│       ├── rsa.py               # RSA public-key encryption
│       └── data/
│           ├── english_dict.txt # English dictionary for language detection
│           └── french_dict.txt  # French dictionary for language detection
├── pyproject.toml               # Modern Python packaging config
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/AstyanM/cryptography-methods.git
cd cryptography-methods

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install the package
pip install -e .
```

## Usage

```bash
# Run as a module
python -m cryptography_methods

# Or use the installed CLI entry point
cryptography-methods
```

You will be presented with an interactive menu:

```
Which encryption method do you want to use ?
1 : Caesar
2 : Transposition
3 : Substitution
4 : Vigenere
5 : One-time Pad
6 : Hash
7 : RSA
8 : Credits
9 : Exit
```

## Technical Details

| Component                | Details                                           |
| ------------------------ | ------------------------------------------------- |
| **Language**             | Python 3.8+                                       |
| **Dependencies**         | `colorama` (terminal colors)                      |
| **RSA primality test**   | Miller-Rabin with 28 rounds                       |
| **RSA key sizes**        | 512 / 768 / 1024-bit prime factors (customizable) |
| **Hash algorithms**      | SHA-256, SHA-512, SHA3-512, MD5, BLAKE2b          |
| **Brute-force charsets** | lowercase, uppercase, digits, printable ASCII     |
| **Dictionary languages** | English, French                                   |

## References

- Singh, S. — _"The Code Book: The Science of Secrecy from Ancient Egypt to Quantum Cryptography"_
- _"La Science des Codes Secrets"_ — Les mysteres de la science
- [Invent with Python — Cracking Codes](http://inventwithpython.com/cracking/) — Transposition cipher decryption
- [Dr. Goulu — Generating Large Primes](https://www.drgoulu.com/2012/04/15/comment-produire-des-nombres-premiers/) — Prime number generation

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Astyan Martin**
