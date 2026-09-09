# |============================|
# |========== BIP-39 ==========|
# |========= by Luca ==========|
# |============================|


import os
import hashlib
import tkinter as tk
from tkinter import filedialog


def bip39_run(Debug, Test, entropy, entropy_bits, Printer_step):

    # File Path
    wordlist_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordlist")
    file_path = filedialog.askopenfilename(title="Select the correct TXT file", initialdir=wordlist_f, filetypes=[("Text files", "*.txt")])

    if file_path:
        # TXT Reading
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"File selected: {file_path}")
    
    else:
        print("No file selecteds.")
    
    # LOADING WORDLIST BIP-39
    def load_wordlist(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
            return words
        
    wordlist = load_wordlist(file_path)
    if Debug:
        print(f"WORD LOADED: {len(wordlist)}\n")

    # SHA-256
    def sha256_bits(data):
        h = hashlib.sha256(data).digest()
        return bin(int.from_bytes(h, "big"))[2:].zfill(256)

    # HEX HASH from SHA256
    hash_hex = hashlib.sha256(entropy).hexdigest()
    # Bytes HASH from SHA256
    hash_bytes = hashlib.sha256(entropy).digest()
    hash_bits = bin(int.from_bytes(hash_bytes, "big"))[2:].zfill(256)
    if Debug:
        print(f"SHA-256: {hash_hex}")
        print(f"SIZE: {len(hash_hex)} char\n")

    # Getting CHECKSUM
    def get_checksum(hash_bits, entropy_bits):
        checksum_length = len(entropy_bits) // 32
        return hash_bits[:checksum_length]

    checksum = get_checksum(hash_bits, entropy_bits)
    full_bits = entropy_bits + checksum
    # Checking lenght
    len(full_bits) == 264

    chunks = [full_bits[i:i+11] for i in range(0, len(full_bits), 11)]
    len(chunks) == 24

    indices = [int(chunk, 2) for chunk in chunks]
    all(0 <= i < 2048 for i in indices)

    mnemonic = [wordlist[i] for i in indices]
    phrase = " ".join(mnemonic)

    # Test Alpha Seed
    if Test:
        # Alpha Seed
        phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"

    print("\n Your SEED PHRASE is been calculated. \n")
    input("Press ENTER to view your seed phrase.\n")
    print(f"SEED PHRASE: \n {phrase} \n")

    # Calculation HEX-SEED
    if Printer_step:
        input("\n Press ENTER to calculate the HEX-SEED.\n")

    mnemonic = phrase
    salt = "mnemonic"

    seed = hashlib.pbkdf2_hmac(
        "sha512",
        mnemonic.encode("utf-8"),
        salt.encode("utf-8"),
        2048,
        dklen=64
    )

    # Showing Hex-Seed
    if Printer_step:
        print(f"HEX-SEED: \n {seed.hex()}")

    # Test Alpha Seed
    if Test:
        seed_hex_Test = "408b285c123836004f4b8842c89324c1f01382450c0d439af345ba7fc49acf705489c6fc77dbd4e3dc1dd8cc6bc9f043db8ada1e243c4a0eafb290d399480840"

        if (seed.hex()==seed_hex_Test):
            print("TEST HEX-SEED: OK")
        else:
            print("TEST HEX-SEED: DOESN'T MATCH!")

    input("\n Press ENTER to continue.\n")

    return seed