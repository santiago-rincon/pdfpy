import os, sys

from colorama import Fore
from PyPDF2 import PdfWriter
import inquirer

def _create_path_pdf(path):
        if not os.path.exists(path) :
            os.makedirs(path)
        return os.path.join(path,'mergepdf.pdf')
    
def _create_folders(path):
    path = os.path.split(path)[0]
    if not os.path.exists(path) :
        os.makedirs(path)


def join(files, output):
    if not files:
        print(f'{Fore.RED}[x] No files provided\n{Fore.YELLOW}[!] For more information try:\n\t{Fore.LIGHTMAGENTA_EX} pdfpy join --help\n')
        sys.exit(1)
    # Convert input files and output file to absolute paths
    files = [os.path.abspath(file) for file in files]
    output = os.path.abspath(output)
    # Check if the output file contains the extension ".pdf"
    if not output.endswith('.pdf'):
        output = _create_path_pdf(output)
    else: 
        _create_folders(output)
    # Check if the output file already exists
    if os.path.exists(output):
        answer = inquirer.prompt([inquirer.Confirm('overwrite', message='The output file already exists. Do you want to overwrite it?')])['overwrite']
        if not answer:
            print(f'{Fore.RED}Change the output file\nFor more information try:\n{Fore.YELLOW}\tpdfpy join --help')
            sys.exit(1)
        else:
            try:
                os.remove(output)
            except OSError as e:
                print(f'{Fore.RED}[-] Failed to remove the output file\n:{e}')
                sys.exit(1)
    # Merge pdf
    merger = PdfWriter()
    for file in files:
        if not file.endswith('.pdf'):
            print(f'{Fore.YELLOW}[!] File "{file}" is not a PDF file. Skipping...')
            continue
        merger.append(file)
    merger.write(output)
    merger.close()
    print(f'{Fore.GREEN}[+] PDF file joined successfully in {output}')

def split(file, pages, split_all, output):
    print(file, pages, split_all, output)