# |===========================|
# |==== ENTROPY GENERATOR ====|
# |========= by Luca =========|
# |===========================|

import secrets


def entropy_generator_run(Debug, Test, Printer_step, entropyVision):

    def entropy_generator(bit=256):
        return secrets.token_bytes(bit//8)

    if not entropyVision:
        entropy = entropy_generator(256)
    else:
        entropy = entropyVision

    if Test:
        print(entropy.hex())
        
    if Debug:
        print(f"ENTROPY:\n{entropy.hex()}\n")
        print("DETAILS:")
        print(f"BITs: {len(entropy)}")

    # ENTROPY TO BITS CONVERSION
    def bits_conv(entropy):
        return bin(int.from_bytes(entropy, "big"))[2:].zfill(len(entropy)*8)

    entropy_bits = bits_conv(entropy)
    if Debug:
        print(f"\nBits conversion:\n{entropy_bits} \n")
        print(f"Lenght: {len(entropy_bits)} bit")

    return entropy, entropy_bits