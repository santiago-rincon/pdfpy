# Import standard libraries
import os, sys, re

# Import local modules
import modules.utilities as utilities

# Import third-party libraries
from colorama import Fore
from PyPDF2 import PdfWriter, PdfReader

def split(file, pages:str, split_all:bool, output):
    # Convert input files and output file to absolute paths
    file = os.path.abspath(file)
    output = os.path.abspath(output)
    # Check if exits pages parameter or flag split_all are specified 
    if not split_all and not pages:
        print(f'{Fore.RED}[x] No pages provided. You must either specify the pages or use the "-a" or "--split-all" parameter to split all pages.\n{Fore.YELLOW}[!] For more information try:\n\t{Fore.LIGHTMAGENTA_EX} pdfpy split --help\n')
        sys.exit(1)
    # Check if the input file contains the extension ".pdf"
    if not file.endswith('.pdf'):
        print(f'{Fore.RED}[x] File "{file}" is not a PDF file.\n\tExiting...')
        sys.exit(1)
    # Check output when --split-all parameter are not specified
    if not split_all:
        # Check if the output file contains the extension ".pdf"
        if not output.endswith('.pdf'):
            output = utilities.create_path_pdf(output,'splited')
        else: 
            utilities.create_folders(output)
        # Check if the output file already exists
        utilities.output_file_exist(output, 'split')
    # Check output when --split-all parameter are specified
    else:
        # Check if the output file contains any extension
        if os.path.splitext(output)[1] and os.path.split(output)[1] != 'splited.pdf':
            print(f'{Fore.RED}[x] The output file must not contain any extension when use the "-a" or "--split-all" parameter, can only be folders.\n\tExiting...')
            sys.exit(1)
        if os.path.split(output)[1] == 'splited.pdf':
            output = os.path.split(output)[0]
        if not os.path.exists(output):
            os.makedirs(output)
    # Split all pages
    pdf_reader = PdfReader(file)
    if split_all:
        if pages:
            print(f'{Fore.YELLOW}[!] Pages argument not required when use the "-a" or "--split-all" parameter. Using all pages...')
        for index, page in enumerate(pdf_reader.pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)
            with open(os.path.join(output,f'page_{index+1}.pdf'), 'wb') as out:
                pdf_writer.write(out)
        print(f'{Fore.GREEN}[+] All pages splited successfully in:\n{output}')
    else:
        # Verify if the pages argument is a string with numbers separated by commas or colons
        if not re.match(r'^[0-9,:]+$', pages):
            print(f'{Fore.RED}[x] The pages argument must be a string with numbers separated by commas or colons. View examples in the help (--help).\n\tExiting...')
            sys.exit(1)
        # Split string with numbers separated by commas
        pages = pages.split(',')
        number_pages=[]
        # Iteration over the pages argument
        for index,page in enumerate(pages):
            if page.isnumeric():
                if index != 0 and int(page) <= number_pages[-1]:
                    print(f'{Fore.RED} Syntax error in "{page}". The number of the page cannot be greater than the number of the previous page.\n\tExiting...')
                    sys.exit(1)
                if int(page) <= len(pdf_reader.pages): 
                    number_pages.append(int(page))
                else:
                    print(f'{Fore.RED} Syntax error in "{page}". The number of the final page cannot be greater than the total number of pages in the file.\n\tExiting...')
                    sys.exit(1)
            else:
                result = utilities.verify_sintax(page,index,pages,len(pdf_reader.pages))
                if type(result) == str:
                    print(Fore.RED + result + '\nView examples in the help (--help).\n\tExiting...')
                    sys.exit(1)
                else: 
                    number_pages.extend(result)
        # Split pages
        pdf_writer = PdfWriter()
        for page in number_pages:
            pdf_writer.add_page(pdf_reader.pages[page-1])
        with open(output, 'wb') as out:
            pdf_writer.write(out)
        print(f'{Fore.GREEN}[+] Pages splited successfully in:\n{output}')
