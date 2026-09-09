# |============================|
# |========== BIP-84 ==========|
# |========= by Luca ==========|
# |============================|


import hashlib



def bip84_run(Debug, Test, child_private_key, private_key_to_compressed_public_key, Printer_step):

    # Compressed Public Key
    public_key = private_key_to_compressed_public_key(
        child_private_key
    )

    if Printer_step:
        print("\nCompressed Public Key (m/84'/0'/0'/0/0):\n", public_key.hex())

    # Test Alpha Seed
    if Test:
        public_key_Test = "03c5db199831f23a3a1575518c8e9e948bfd495481aac442dec64b447ee76bd6fa"
        if (public_key.hex() == public_key_Test):
            print("TEST Public Key: OK")
        else:
            print("TEST Public Key: DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")

    # HASH160 of Compressed Public Key
    sha256_hash = hashlib.sha256(public_key).digest()
    hash160 = hashlib.new("ripemd160", sha256_hash).digest()

    if Printer_step:
        print("\nSHA-256:", sha256_hash.hex())
        print("HASH160:", hash160.hex())

    # Test Alpha Seed
    if Test:
        hash160_Test = "16d630413cea75fd5ad88433cd815ae5ba1ba645"
        if (hash160.hex() == hash160_Test):
            print("TEST HASH160: OK")
        else:
            print("TEST HASH160: DOESN'T MATCH!")

    if Printer_step:
        input("\n Press ENTER to continue.\n")


    # BECH32

    def convertbits(data, frombits, tobits, pad=True):
        acc = 0
        bits = 0
        ret = []
        maxv = (1 << tobits) - 1

        for value in data:
            if value < 0 or (value >> frombits):
                return None

            acc = (acc << frombits) | value
            bits += frombits

            while bits >= tobits:
                bits -= tobits
                ret.append((acc >> bits) & maxv)

        if pad:
            if bits:
                ret.append((acc << (tobits - bits)) & maxv)
        elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
            return None

        return ret


    BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

    def bech32_polymod(values):
        generator = [
            0x3b6a57b2,
            0x26508e6d,
            0x1ea119fa,
            0x3d4233dd,
            0x2a1462b3
        ]

        chk = 1

        for value in values:
            top = chk >> 25
            chk = ((chk & 0x1ffffff) << 5) ^ value

            for i in range(5):
                if (top >> i) & 1:
                    chk ^= generator[i]

        return chk


    def bech32_hrp_expand(hrp):
        return (
            [ord(char) >> 5 for char in hrp]
            + [0]
            + [ord(char) & 31 for char in hrp]
        )


    def bech32_create_checksum(hrp, data):
        values = (
            bech32_hrp_expand(hrp)
            + data
            + [0, 0, 0, 0, 0, 0]
        )

        polymod = bech32_polymod(values) ^ 1

        return [
            (polymod >> 5 * (5 - i)) & 31
            for i in range(6)
        ]


    def bech32_encode(hrp, data):
        combined = data + bech32_create_checksum(hrp, data)

        return hrp + "1" + "".join(
            BECH32_CHARSET[value]
            for value in combined
        )

    # Address creation
    witness_version = 0

    witness_program = hash160

    converted_program = convertbits(
        witness_program,
        8,
        5,
        True
    )

    bech32_data = [witness_version] + converted_program

    address = bech32_encode(
        "bc",
        bech32_data
    )

    if Printer_step:
        print("\nBitcoin Address (BIP-84):", address)

    # Test Alpha Seed
    if Test:
        address_Test = "bc1qzmtrqsfuaf6l6kkcsseumq26ukaphfj9skkug6"
        if (address == address_Test):
            print("TEST address: OK")
        else:
            print("TEST address: DOESN'T MATCH!")

    return address