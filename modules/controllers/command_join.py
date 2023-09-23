# Import standard libraries
import os, sys

# Import local modules 
import modules.utilities as utilities

# Import third-party libraries
from colorama import Fore
from PyPDF2 import PdfWriter

def join(files, output):
    if not files:
        print(f'{Fore.RED}[x] No files provided\n{Fore.YELLOW}[!] For more information try:\n\t{Fore.LIGHTMAGENTA_EX} pdfpy join --help\n')
        sys.exit(1)
    # Convert input files and output file to absolute paths
    files = [os.path.abspath(file) for file in files]
    output = os.path.abspath(output)
    # Check if the output file contains the extension ".pdf"
    if not output.endswith('.pdf'):
        output = utilities.create_path_pdf(output,'merged')
    else: 
        utilities.create_folders(output)
    # Check if the output file already exists
    utilities.output_file_exist(output, 'join')
    # Merge pdf
    merger = PdfWriter()
    for file in files:
        if not file.endswith('.pdf'):
            print(f'{Fore.YELLOW}[!] File "{file}" is not a PDF file.\n\tSkipping...')
            continue
        merger.append(file)
    merger.write(output)
    merger.close()
    print(f'{Fore.GREEN}[+] PDF file joined successfully in:\n{output}')
