import os, sys, re
from colorama import Fore
from PyPDF2 import PdfWriter, PdfReader
import inquirer


def _create_path_pdf(path,name:str):
    if os.path.isfile(path):
        print(f'{Fore.RED}[x] The path "{path}" is a file. Please provide a folder path or pdf file path.')
        sys.exit(1)
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path,f'{name}.pdf')
    
def _create_folders(path):
    path = os.path.split(path)[0]
    if not os.path.exists(path) :
        os.makedirs(path)

def _output_file_exist(path, command:str):
    if os.path.exists(path):
        answer = inquirer.prompt([inquirer.Confirm('overwrite', message='The output file already exists. Do you want to overwrite it?')])['overwrite']
        if not answer:
            print(f'{Fore.RED}Change the output file\nFor more information try:\n{Fore.YELLOW}\tpdfpy {command} --help')
            sys.exit(1)
        else:
            try:
                os.remove(path)
            except OSError as e:
                print(f'{Fore.RED}[-] Failed to remove the output file\n:{e}')
                sys.exit(1)

def _verify_sintax(sintax:str, index:int, array, pages_lenght):
    if re.fullmatch(r'\d+:+\d+:+\d+',sintax):
        # 4:2:10
        query = sintax.split(':')
        if int(query[0]) > int(query[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the number of the final page.'
        if int(query[-1])> pages_lenght: return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(int(query[0]),int(query[2])+1, int(query[1])))
    elif re.fullmatch(r'^:+\d+',sintax):
        # :10
        query = sintax.split(':')
        if index != 0: return f'Syntax error in "{sintax}". When you use a colon at the beginning there cannot be a previous number.'
        if int(query[-1])> pages_lenght: return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(1,int(query[-1])+1))
    elif re.fullmatch(r'^\d+:+\d+$',sintax):
        # 4:10
        query = sintax.split(':')
        if int(query[0]) >= int(query[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be greater or equal than the number of the final page.'
        if int(query[-1])> pages_lenght: return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(int(query[0]),int(query[-1])+1))
    elif re.fullmatch(r'^\d+:$',sintax):
        # 4:
        query = sintax.split(':')
        if int(query[0]) > pages_lenght: return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1: f'Syntax error in "{sintax}". When you use a colon at the end, there cannot be a trailing number.'
        return list(range(int(query[0]),pages_lenght+1))
    elif re.fullmatch(r'^\d+:+\d+:$', sintax):
        # 4:2:
        query = sintax.split(':')
        if int(query[0]) > pages_lenght: return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]): return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1: f'Syntax error in "{sintax}". When you use a colon at the end, there cannot be a trailing number.'
        return list(range(int(query[0]),pages_lenght+1, int(query[1])))
    elif re.fullmatch(r'^:\d+:\d+$', sintax):
        # :5:14
        query = sintax.split(':')
        if index != 0: return f'Syntax error in "{sintax}". When you use a colon at the beginning there cannot be a previous number.'
        if int(query[-1])> pages_lenght: return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]): return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(1,int(query[-1])+1, int(query[1])))
    elif re.fullmatch(r'^:\d+:$', sintax):
        if index != 0 or len(array) !=1 : return f'Syntax error in "{sintax}". When a colon is used at the beginning or at the end, there cannot be numbers before or after it.'
        return list(range(1,pages_lenght+1, int(sintax.split(':')[1])))
    else:
        return f'Syntax error in "{sintax}"'

def join(files, output):
    if not files:
        print(f'{Fore.RED}[x] No files provided\n{Fore.YELLOW}[!] For more information try:\n\t{Fore.LIGHTMAGENTA_EX} pdfpy join --help\n')
        sys.exit(1)
    # Convert input files and output file to absolute paths
    files = [os.path.abspath(file) for file in files]
    output = os.path.abspath(output)
    # Check if the output file contains the extension ".pdf"
    if not output.endswith('.pdf'):
        output = _create_path_pdf(output,'merged')
    else: 
        _create_folders(output)
    # Check if the output file already exists
    _output_file_exist(output, 'join')
    # Merge pdf
    merger = PdfWriter()
    for file in files:
        if not file.endswith('.pdf'):
            print(f'{Fore.YELLOW}[!] File "{file}" is not a PDF file.\n\tSkipping...')
            continue
        merger.append(file)
    merger.write(output)
    merger.close()
    print(f'{Fore.GREEN}[+] PDF file joined successfully in {output}')

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
            output = _create_path_pdf(output,'splited')
        else: 
            _create_folders(output)
        # Check if the output file already exists
        _output_file_exist(output, 'split')
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
        print(f'{Fore.GREEN}[+] All pages splited successfully in {output}')
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
                result = _verify_sintax(page,index,pages,len(pdf_reader.pages))
                if type(result) == str:
                    print(Fore.RED + result + '\nView examples in the help (--help).\n\tExiting...')
                    sys.exit(1)
                else: 
                    number_pages.extend(result)
        
        pdf_writer = PdfWriter()
        for page in number_pages:
            pdf_writer.add_page(pdf_reader.pages[page-1])
        with open(output, 'wb') as out:
            pdf_writer.write(out)
        print(f'{Fore.GREEN}[+] Pages splited successfully in {output}')