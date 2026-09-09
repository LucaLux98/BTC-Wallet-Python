# Optical Entropy Bitcoin Wallet Generator
(BIP-39 / BIP-32 / BIP-84)

An air-gapped, deterministic Bitcoin wallet generator implemented in Python.
The tool harvests physical entropy from image files using Computer Vision and Morphological Analysis (OpenCV), then derives standard BIP-84 Native SegWit (`bc1...`) addresses through strict BIP-39 mnemonic encoding and BIP-32 hierarchical deterministic (HD) key derivation.



-----



## Key Features

Computer Vision Entropy Harvester: Extracts non-deterministic entropy from arbitrary images by splitting color channels (RGB + Grayscale), partitioning into a 4x4 matrix, thresholding, and calculating morphological invariants (contour area, perimeter, bounding box metrics, circularity);
BIP-39 Mnemonic Encoding: Converts 256 bits of entropy + 8-bit checksum into a 24-word seed phrase, with multi-language dictionary support (English, Italian, Spanish, French, Portuguese, Czech, Simplified Chinese, Traditional Chinese, Japanese, Korean);
Cryptographic Seed Derivation: Uses PBKDF2-HMAC-SHA512 (2048 iterations) to derive a 512-bit master binary seed;
BIP-32 HD Key Derivation: Implements hierarchical deterministic derivation over the `secp256k1` elliptic curve for hardened and non-hardened child keys;
BIP-84 Native SegWit Compliance: Derives paths following `m/84'/0'/0'/0/index` and encodes public key hashes into standard Bech32 (`bc1q...`) addresses without relying on black-box wallet libraries;
Air-Gap Security Focused: Built-in verification prompts to enforce execution in fully offline/air-gapped environments.



---



## Technical Architecture & Pipeline


(Image Input) ► [ Morphological Features Extraction ] ► (Entropy) ► [ BIP-39 ] ► (Seed Phrase) ► [ BIP-32 ] ► [ BIP-84 ] ► (Address)



---



## Repository Structure


```text

├── bip32.py                         # Hierarchical Deterministic wallet derivation (secp256k1)
├── bip39.py                         # Entropy checksumming, wordlist indexing, PBKDF2 hashing
├── bip84.py                         # HASH160 and Bech32 address encoder (Native SegWit)
├── dist/
│	 ├── main.exe			         # Standalone pre-compiled binary for offline Windows execution (portable)
├── entropy_generation_VisionAI.py   # Image-based feature extraction and entropy generation
├── entropy_generator.py             # CSPRNG fallback and bit conversion utilities
├── main.py                          # CLI orchestrator and offline safety checks
├── wordlist/                        # Official BIP-39 dictionaries (multi-language TXT files)
│    ├── english.txt
│    ├── italian.txt
│    ├── spanish.txt
│    └── ...
└── img/

```


---



## Tech Stack & Dependencies

Language: Python 3.9+
Cryptographic Primitives: hashlib, hmac, secrets (standard library)
Elliptic Curve Operations: ecdsa (SECP256k1)
Image Processing & Computer Vision: opencv-python, numpy
GUI / File Selection: tkinter



---



## Getting Started

Clone & Setup Environment

```text
git clone [https://github.com/yourusername/btc-vision-wallet-generator.git](https://github.com/yourusername/btc-vision-wallet-generator.git)
cd btc-vision-wallet-generator

python -m venv venv

# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

2. Requirements
```text
ecdsa >= 0.18.0
numpy >= 1.24.0
opencv-python >= 4.8.0
```
3. Execution

Recommendation: Run this software on an air-gapped machine (offline OS / live USB) when generating production keys.
```text
python main.py
```


---



## HOW TO USE /!\


1. Confirm offline status;

2. Choose entropy source (1 for Image/VisionAI, 0 for system CSPRNG);

3. Select your image for entropy;

4. Select your preferred language wordlist from the wordlist directory;

5. Retrieve your SEED PHRASE (24-word recovery phrase) printed;

6. Input target address index (e.g. 1 for first receiving address m/84'/0'/0'/0/0);

7. Retrieve your Bech32 address (e.g. bc1q***).



---



## Verification & Standards Compliance

The core cryptographic modules (bip32.py, bip39.py, bip84.py) contain integrated test fixtures using official Bitcoin test vectors (e.g. test seed abandon... art). Derivation paths, intermediate chain codes, and final Bech32 outputs have been cross-verified against BIP specifications.



---



## DISCLAIMER /!\ /!\ /!\

This software is designed for educational and cryptographic research purposes. When handling real funds, always ensure keys are generated on verified, tamper-proof, air-gapped hardware.
