# -- FILE ENCRYPTION / DECRYPTION --
# Two methods:
#   1. Caesar cipher  — shifts every letter by a fixed number (simple, educational)
#   2. Fernet         — real cryptographic encryption (secure, production-ready)


import os
from cryptography.fernet import Fernet   # pip install cryptography


# ══════════════════════════════════════════════════════════════════════════════
#  METHOD 1 — CAESAR CIPHER
#  Concept: every letter in the alphabet is shifted forward by `key` positions.
#  A with key=3 becomes D. Z wraps around to C.
#  To decrypt, you just shift backward by the same key.
#
#  Limitation: only 25 possible keys, easily cracked by trying all of them.
#  Good for learning the concept; NOT secure for real use.
# ══════════════════════════════════════════════════════════════════════════════

def caesar_encrypt(text, key):
    """
    Encrypt a string by shifting every letter forward by `key` positions.
    Non-letter characters (spaces, punctuation, numbers) are left unchanged.
    """
    result = []

    for char in text:
        # We handle uppercase and lowercase separately so 'A' stays 'A' style
        # and 'a' stays 'a' style after shifting.

        if char.isupper():
            # ord() converts a character to its ASCII number. ord('A') = 65.
            # Subtracting ord('A') gives us a 0-25 position (A=0, B=1, ..., Z=25).
            # Adding `key` shifts forward. % 26 wraps around past Z back to A.
            # Adding ord('A') converts the number back to a character.
            shifted = (ord(char) - ord('A') + key) % 26 + ord('A')
            result.append(chr(shifted))   # chr() converts a number back to a character

        elif char.islower():
            shifted = (ord(char) - ord('a') + key) % 26 + ord('a')
            result.append(chr(shifted))

        else:
            # Not a letter — leave it exactly as is
            result.append(char)

    return ''.join(result)   # join the list of characters into a single string


def caesar_decrypt(text, key):
    """
    Decrypt by shifting backward. Shifting forward by (26 - key) is
    mathematically the same as shifting backward, without needing negative numbers.
    """
    return caesar_encrypt(text, 26 - key)


def caesar_encrypt_file(input_path, output_path, key):
    """Read a text file, encrypt it with Caesar cipher, save to a new file."""
    try:
        file = open(input_path, 'r', encoding='utf-8')
        content = file.read()
        file.close()
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return False

    encrypted = caesar_encrypt(content, key)

    file = open(output_path, 'w', encoding='utf-8')
    file.write(encrypted)
    file.close()

    print(f"Encrypted → '{output_path}' (Caesar, key={key})")
    return True


def caesar_decrypt_file(input_path, output_path, key):
    """Read an encrypted file, decrypt it, save the original content."""
    try:
        file = open(input_path, 'r', encoding='utf-8')
        content = file.read()
        file.close()
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return False

    decrypted = caesar_decrypt(content, key)

    file = open(output_path, 'w', encoding='utf-8')
    file.write(decrypted)
    file.close()

    print(f"Decrypted → '{output_path}' (Caesar, key={key})")
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  METHOD 2 — FERNET ENCRYPTION
#  Fernet is a symmetric encryption standard from the `cryptography` library.
#  Symmetric means: the same key encrypts AND decrypts (like a physical key).
#
#  How it works:
#    1. generate_key() creates a random 256-bit key (very hard to guess)
#    2. encrypt() turns your text into scrambled bytes — looks like garbage
#    3. decrypt() with the SAME key perfectly restores the original
#
#  The key is saved to a file ('secret.key') so you can decrypt later.
#  Losing the key means the file is permanently unreadable — there's no backdoor.
# ══════════════════════════════════════════════════════════════════════════════

KEY_FILE = 'secret.key'   # where the Fernet key is saved on disk


def generate_key():
    """
    Generate a new random Fernet key and save it to KEY_FILE.
    Only do this once — if you overwrite the key, old encrypted files
    become permanently unreadable.
    """
    if os.path.exists(KEY_FILE):
        # os.path.exists() checks if a file already exists without crashing.
        print(f"Key file '{KEY_FILE}' already exists. Using existing key.")
        return

    key = Fernet.generate_key()
    # generate_key() produces a random URL-safe base64-encoded 32-byte key.
    # It looks like: b'abc123XYZ...' — a bytes object, not a plain string.

    file = open(KEY_FILE, 'wb')   # 'wb' = write bytes (not text)
    file.write(key)
    file.close()
    print(f"New key generated and saved to '{KEY_FILE}'.")


def load_key():
    """
    Load the Fernet key from disk. The key must exist before encrypt/decrypt.
    Returns the key as bytes, or None if the file doesn't exist.
    """
    if not os.path.exists(KEY_FILE):
        print(f"Error: key file '{KEY_FILE}' not found. Run 'Generate key' first.")
        return None

    file = open(KEY_FILE, 'rb')   # 'rb' = read bytes
    key = file.read()
    file.close()
    return key


def fernet_encrypt_file(input_path, output_path):
    """
    Read a text file, encrypt it with Fernet, save ciphertext to output_path.
    The output is binary (not readable text), so we open files in bytes mode.
    """
    key = load_key()
    if key is None:
        return False

    # Fernet(key) creates an encryptor/decryptor object loaded with the key.
    f = Fernet(key)

    try:
        file = open(input_path, 'rb')   # read as bytes — Fernet works on bytes
        data = file.read()
        file.close()
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return False

    encrypted_data = f.encrypt(data)
    # f.encrypt() returns bytes. The result starts with 'gAAAAA...' — a
    # timestamp + encrypted payload + authentication tag. The auth tag means
    # if anyone tampers with the file, decryption fails instead of silently
    # returning wrong data. This is what makes Fernet trustworthy.

    file = open(output_path, 'wb')   # write as bytes
    file.write(encrypted_data)
    file.close()

    print(f"Encrypted → '{output_path}' (Fernet)")
    return True


def fernet_decrypt_file(input_path, output_path):
    """
    Read a Fernet-encrypted file, decrypt it, save the original content.
    """
    key = load_key()
    if key is None:
        return False

    f = Fernet(key)

    try:
        file = open(input_path, 'rb')
        encrypted_data = file.read()
        file.close()
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return False

    try:
        decrypted_data = f.decrypt(encrypted_data)
        # f.decrypt() raises InvalidToken if:
        #   - the key is wrong
        #   - the file was tampered with
        #   - the data isn't a valid Fernet token at all
    except Exception:
        print("Error: decryption failed. Wrong key or corrupted file.")
        return False

    file = open(output_path, 'wb')
    file.write(decrypted_data)
    file.close()

    print(f"Decrypted → '{output_path}' (Fernet)")
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  MENU
# ══════════════════════════════════════════════════════════════════════════════

def get_key_number():
    """Prompt until the user enters a valid integer for the Caesar key."""
    while True:
        try:
            return int(input("Enter shift key (1-25): "))
        except ValueError:
            print("Please enter a number.")


def main():
    print("=== File Encryption / Decryption ===\n")

    while True:
        print("─" * 36)
        print("Method 1 — Caesar cipher")
        print("  1. Encrypt file (Caesar)")
        print("  2. Decrypt file (Caesar)")
        print("Method 2 — Fernet (secure)")
        print("  3. Generate encryption key")
        print("  4. Encrypt file (Fernet)")
        print("  5. Decrypt file (Fernet)")
        print("  6. Quit")
        print("─" * 36)

        choice = input("Choose option: ").strip()

        if choice == '1':
            src = input("Input file path:  ")
            dst = input("Output file path: ")
            key = get_key_number()
            caesar_encrypt_file(src, dst, key)

        elif choice == '2':
            src = input("Input file path:  ")
            dst = input("Output file path: ")
            key = get_key_number()
            caesar_decrypt_file(src, dst, key)

        elif choice == '3':
            generate_key()

        elif choice == '4':
            src = input("Input file path:  ")
            dst = input("Output file path: ")
            fernet_encrypt_file(src, dst)

        elif choice == '5':
            src = input("Input file path:  ")
            dst = input("Output file path: ")
            fernet_decrypt_file(src, dst)

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1–6.")

        print()


if __name__ == '__main__':
    main()