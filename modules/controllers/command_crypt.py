# Import standard libraries
import os
import sys

# Import local modules
import modules.utilities as utilities

# Import third-party libraries
from colorama import Fore
from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.errors import FileNotDecryptedError


def crypt(file, mode, password, output):
    # Convert input file to absolute path
    file = os.path.abspath(file)
    # Check if the input file contains the extension ".pdf"
    utilities.check_extension_input_file(file)
    if output:
        # Convert output file to absolute path
        output = os.path.abspath(output)
        # Check if the output file contains the extension ".pdf"
        if not output.endswith('.pdf'):
            output = utilities.create_path_pdf(output, mode)
        # Check if the output file already exists
        utilities.output_file_exist(output, 'crypt')
    else:
        output = os.path.join(os.getcwd(), f'{mode}.pdf')
    # Create PDF objects to read and write
    reader = PdfReader(file)
    writer = PdfWriter()
    if mode == 'encrypt':
        # Encrypt PDF
        writer.encrypt(password)
    elif mode == 'decrypt':
        # Check if the file is encrypted
        if not reader.is_encrypted:
            print(f'{Fore.RED}[-] The file "{file}" is not encrypted.')
            sys.exit(1)
        # Decrypt PDF
        reader.decrypt(password)
    try:
        for page in reader.pages:
            writer.add_page(page)
        # Save PDF
        with open(output, 'wb') as out:
            writer.write(out)
        print(f'{Fore.GREEN}[+] File {mode} was saved in:\n{output}')
    except FileNotDecryptedError:
        print(f'{Fore.RED}[-] The password is incorrect.')
        sys.exit(1)
