# |=================================================================|
# |========= Tool to convert your entrophy in a BTC Wallet =========|
# |========================= by LucaLux98 ==========================|
# |=================================================================|

# |=====================================|
# |-------------- INDEX ----------------|
# |                                     |
# |  10-43      [ INITIALIZATION ]      |
# |  44-134         [BIP-39]            |
# | 135-X           [BIP-32]            |
# |                                     |
# |=====================================|


import entropy_generator
import entropy_generation_VisionAI
import bip39
import bip32
import bip84


Debug = 0
Test = 0
Printer_step = 0


print("This is a tool to convert your entrophy in a BTC Wallet \n")
print("Attention! Before you begin, make sure that your device is disconected from the internet!")

# ONLINE/OFFLINE CHECKS
def on_off_checks():
    print("Did you start this program OFFLINE?")
    while True:
        A = int(input("1 = Yes, 0 = No: "))
        if A == 1:
            print("Perfect! Safety is guaranteed.\n")
            return True
        elif A == 0:
            print("ATTENTION: Turn OFF the internet before continue!")
            print("TURN OFF INTERNET AND TRY AGAIN!")
            print("Program restarted \n")
            print("Did you start this program OFFLINE?")
        else:
            print("\n ERROR: Wrong input, try again:")
    
# CHECK LUNCH
on_off_checks()

# ENTROPY GENERATION
print("Do you want to generate an ENTROPY with VisionAI (Recommended) or with a Random Generator (ONLY FOR TESTING)?")
EG = int(input("1 = VisionAI / 0 = Random Generator: "))
if EG == 0:
    entropy, entropy_bits = entropy_generator.entropy_generator_run(Debug, Test, Printer_step, entropyVision=None)
else:
    entropy = entropy_generation_VisionAI.entropy_generation_VisionAI_run(Debug, Test, Printer_step)
    entropy, entropy_bits = entropy_generator.entropy_generator_run(Debug, Test, Printer_step, entropyVision = entropy)

# BIP-39
seed = bip39.bip39_run(Debug, Test, entropy, entropy_bits, Printer_step)

# USER INPUTS
while True:
    Address_Num = int(input("Write the BTC address do you want to generate (1-10...): "))
    if Address_Num < 1:
        print("ERROR: Address number must be greater than 0. Program restarted \n")
    else:
        break

# BIP-32
child_private_key, private_key_to_compressed_public_key = bip32.bip32_run(Debug, Test, seed, Address_Num, Printer_step)

# BIP-84
address = bip84.bip84_run(Debug, Test, child_private_key, private_key_to_compressed_public_key, Printer_step)

# PRINTING FINAL RESULTS
print("BTC Wallet generated successfully!")
input("\n Press ENTER to see your ADDRESS.\n \n")
print(f"Address: {address}\n")

# END PROGRAM
input("\n PRESS ENTER TO EXIT \n")