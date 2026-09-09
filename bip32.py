# |============================|
# |========== BIP-32 ==========|
# |========= by Luca ==========|
# |============================|


import hmac
import hashlib
import struct
from ecdsa import SigningKey, SECP256k1



def bip32_run(Debug, Test, seed, Address_Num, Printer_step):
    
    # Master Private Key and Master Chain Code
    I = hmac.new(
        key=b"Bitcoin seed",
        msg=seed,
        digestmod=hashlib.sha512
    ).digest()

    master_private_key = I[:32]
    master_chain_code = I[32:]

    if Printer_step:
        print("Master Private Key:", master_private_key.hex())
        print("Master Chain Code: ", master_chain_code.hex())

    # Test Alpha Seed
    if Test:
        MPK_Test = "235b34cd7c9f6d7e4595ffe9ae4b1cb5606df8aca2b527d20a07c8f56b2342f4"
        MCC_Test = "f40eaad21641ca7cb5ac00f9ce21cac9ba070bb673a237f7bce57acda54386a4"

        if (master_private_key.hex()==MPK_Test):
            print("TEST Master Private Key: OK")
        else:
            print("TEST Master Private Key: DOESN'T MATCH!")

        if (master_chain_code.hex()==MCC_Test):
            print("TEST Master Chain Code: OK")
        else:
            print("TEST Master Chain Code: DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")

    SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    def private_key_to_compressed_public_key(private_key):
        # Crea la signing key dalla private key
        signing_key = SigningKey.from_string(
            private_key,
            curve=SECP256k1
        )

        # Ottiene la public key non compressa (64 byte: X + Y)
        public_key = signing_key.get_verifying_key()

        public_key_bytes = public_key.to_string()

        # Dividi X e Y
        x = public_key_bytes[:32]
        y = public_key_bytes[32:]

        # Compressed public key:
        # 02 if Y is even
        # 03 if Y is odd
        prefix = b"\x02" if (int.from_bytes(y, "big") % 2 == 0) else b"\x03"

        return prefix + x

    def derive_child_private_key(parent_private_key, parent_chain_code, index):
        # INDEX 32 bit, format big-endian
        index_bytes = struct.pack(">L", index)

        # Hardened derivation
        if index >= 2**31:
            data = b"\x00" + parent_private_key + index_bytes
        # NOT-Hardened derivation
        else:
            parent_public_key = private_key_to_compressed_public_key(parent_private_key)
            data = parent_public_key + index_bytes


        # HMAC-SHA512
        I = hmac.new(
            key=parent_chain_code,
            msg=data,
            digestmod=hashlib.sha512
        ).digest()

        # Result derivation in 2 parts
        IL = I[:32]
        IR = I[32:]

        # Convert bytes to integers
        IL_int = int.from_bytes(IL, byteorder="big")
        parent_int = int.from_bytes(parent_private_key, byteorder="big")

        # Calculate Child Private Key
        child_int = (IL_int + parent_int) % SECP256K1_ORDER

        # Convert the result back to 32 bytes
        child_private_key = child_int.to_bytes(32, byteorder="big")

        # IR becomes the new Chain Code
        child_chain_code = IR

        return child_private_key, child_chain_code

    # DERIVAZIONI
    # m/84' - (Native SegWit)
    index = 84 + 2**31

    child_private_key, child_chain_code = derive_child_private_key(
        master_private_key,
        master_chain_code,
        index
    )

    if Printer_step:
        print("\nChild Private Key (m/84'):", child_private_key.hex())
        print("Child Chain Code (m/84'):", child_chain_code.hex())
    

    # Test Alpha Seed
    if Test:
        CPK_84_Test = "58416d672192cbe570589448c984cbbbe0f742b6b219ba5f8694b4a5cc9b6566"
        CCC_84_Test = "e893469ad3af0a4d38c38df7bf29e2a5dced05b9a9f0018e11d710a0a5f17751"

        if (child_private_key.hex()==CPK_84_Test):
            print("TEST Child Private Key (m/84'): OK")
        else:
            print("TEST Child Private Key (m/84'): DOESN'T MATCH!")

        if (child_chain_code.hex()==CCC_84_Test):
            print("TEST Child Chain Code (m/84'): OK")
        else:
            print("TEST Child Chain Code (m/84'): DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")


    # m/84'/0' - (Bitcoin Mainnet)
    index = 0 + 2**31

    child_private_key, child_chain_code = derive_child_private_key(
        child_private_key,
        child_chain_code,
        index
    )

    if Printer_step:
        print("\nChild Private Key (m/84'/0'):", child_private_key.hex())
        print("Child Chain Code (m/84'/0'):", child_chain_code.hex())

    # Test Alpha Seed
    if Test:
        CPK_84_0_Test = "db70971dd2d65cc15cf09eb614bc3d52d77bfe797c1c1be6d8600fd0eeb9302a"
        CCC_84_0_Test = "d61f7a78bfa97edabec33874023feaadf1fdd9b46b9c1254587ac13d680ffbbf"

        if (child_private_key.hex()==CPK_84_0_Test):
            print("TEST Child Private Key (m/84'/0'): OK")
        else:
            print("TEST Child Private Key (m/84'/0'): DOESN'T MATCH!")

        if (child_chain_code.hex()==CCC_84_0_Test):
            print("TEST Child Chain Code (m/84'/0'): OK")
        else:
            print("TEST Child Chain Code (m/84'/0'): DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")


    # m/84'/0'/0' - (Account 0)
    index = 0 + 2**31

    child_private_key, child_chain_code = derive_child_private_key(
        child_private_key,
        child_chain_code,
        index
    )

    if Printer_step:
        print("\nChild Private Key (m/84'/0'/0'):", child_private_key.hex())
        print("Child Chain Code (m/84'/0'/0'): ", child_chain_code.hex())

    # Test Alpha Seed
    if Test:
        CPK_84_0_0_Test = "57558e8c90c2e72f0c121d0fb8844bbbe7a872f0065d21b218a990450b9f93be"
        CCC_84_0_0_Test = "9220117c4fa030015437ab195732bd1dd2d0f0f07f4dcaaf51350b25bc5a3c82"

        if child_private_key.hex() == CPK_84_0_0_Test:
            print("TEST Child Private Key (m/84'/0'/0'): OK")
        else:
            print("TEST Child Private Key (m/84'/0'/0'): DOESN'T MATCH!")

        if child_chain_code.hex() == CCC_84_0_0_Test:
            print("TEST Child Chain Code (m/84'/0'/0'): OK")
        else:
            print("TEST Child Chain Code (m/84'/0'/0'): DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")


    # m/84'/0'/0'/0 - (External chain)
    index = 0

    child_private_key, child_chain_code = derive_child_private_key(
        child_private_key,
        child_chain_code,
        index
    )

    if Printer_step:
        print("\nChild Private Key (m/84'/0'/0'/0):", child_private_key.hex())
        print("Child Chain Code (m/84'/0'/0'/0):", child_chain_code.hex())

    # Test Alpha Seed
    if Test:
        CPK_84_0_0_0_Test = "3fab5a69df7525373aa30dacaf2e31ba9f2c0e96f4cd4b5d366981d026cfcebb"
        CCC_84_0_0_0_Test = "71e01012bf95f5f586e16ca3c3bdbf9c56731a52fc14db800facf664dac01774"

        if child_private_key.hex() == CPK_84_0_0_0_Test:
            print("TEST Child Private Key (m/84'/0'/0'/0): OK")
        else:
            print("TEST Child Private Key (m/84'/0'/0'/0): DOESN'T MATCH!")

        if child_chain_code.hex() == CCC_84_0_0_0_Test:
            print("TEST Child Chain Code (m/84'/0'/0'/0): OK")
        else:
            print("TEST Child Chain Code (m/84'/0'/0'/0): DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")


    # m/84'/0'/0'/0/0 - (Address index 0)
    index = Address_Num - 1

    child_private_key, child_chain_code = derive_child_private_key(
        child_private_key,
        child_chain_code,
        index
    )

    if Printer_step:
        print("\nChild Private Key (m/84'/0'/0'/0/0):", child_private_key.hex())
        print("Child Chain Code (m/84'/0'/0'/0/0):", child_chain_code.hex())

    # Test Alpha Seed
    if Test:
        CPK_84_0_0_0_0_Test = "0cde867159a5bbda96fe61d5ddfadc2ac306c8cc49cbe90a9571a6092fbb1a20"
        CCC_84_0_0_0_0_Test = "b62332af3bc253eef2efe4d65b4911c5573827a9a3ec48f59b9b6f3004562ca0"

        if child_private_key.hex() == CPK_84_0_0_0_0_Test:
            print("TEST Child Private Key (m/84'/0'/0'/0/0): OK")
        else:
            print("TEST Child Private Key (m/84'/0'/0'/0/0): DOESN'T MATCH!")

        if child_chain_code.hex() == CCC_84_0_0_0_0_Test:
            print("TEST Child Chain Code (m/84'/0'/0'/0/0): OK")
        else:
            print("TEST Child Chain Code (m/84'/0'/0'/0/0): DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")

    return child_private_key, private_key_to_compressed_public_key