# Import standard libraries
import os
import sys
import re

# Import third-party libraries
import inquirer
from colorama import Fore


def create_path_pdf(path, name: str):
    if os.path.isfile(path):
        print(
            f'{Fore.RED}[x] The path "{path}" is a file. Please provide a folder path or pdf file path.')
        sys.exit(1)
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, f'{name}.pdf')


def create_folders(path):
    path = os.path.split(path)[0]
    if not os.path.exists(path):
        os.makedirs(path)


def output_file_exist(path, command: str):
    if os.path.exists(path):
        answer = inquirer.prompt([inquirer.Confirm(
            'overwrite', message='The output file already exists. Do you want to overwrite it?')])['overwrite']
        if not answer:
            print(
                f'{Fore.RED}Change the output file\nFor more information try:\n{Fore.YELLOW}\tpdfpy {command} --help')
            sys.exit(1)
        else:
            try:
                os.remove(path)
            except OSError as e:
                print(f'{Fore.RED}[-] Failed to remove the output file\n:{e}')
                sys.exit(1)


def verify_sintax(sintax: str, index: int, array, pages_lenght):
    if re.fullmatch(r'\d+:+\d+:+\d+', sintax):
        # 4:2:10
        query = sintax.split(':')
        if int(query[0]) > int(query[-1]):
            return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the number of the final page.'
        if int(query[-1]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(int(query[0]), int(query[2])+1, int(query[1])))
    elif re.fullmatch(r'^:+\d+', sintax):
        # :10
        query = sintax.split(':')
        if index != 0:
            return f'Syntax error in "{sintax}". When you use a colon at the beginning there cannot be a previous number.'
        if int(query[-1]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(1, int(query[-1])+1))
    elif re.fullmatch(r'^\d+:+\d+$', sintax):
        # 4:10
        query = sintax.split(':')
        if int(query[0]) >= int(query[-1]):
            return f'Syntax error in "{sintax}". The number of the initial page cannot be greater or equal than the number of the final page.'
        if int(query[-1]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(int(query[0]), int(query[-1])+1))
    elif re.fullmatch(r'^\d+:$', sintax):
        # 4:
        query = sintax.split(':')
        if int(query[0]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            f'Syntax error in "{sintax}". When you use a colon at the end, there cannot be a trailing number.'
        return list(range(int(query[0]), pages_lenght+1))
    elif re.fullmatch(r'^\d+:+\d+:$', sintax):
        # 4:2:
        query = sintax.split(':')
        if int(query[0]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the initial page cannot be greater than the total number of pages in the file.'
        if index != 0:
            if array[index-1].isnumeric():
                if int(query[0]) <= int(array[index-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
            else:
                if int(query[0]) <= int(array[index-1].split(':')[-1]):
                    return f'Syntax error in "{sintax}". The number of the initial page cannot be less or equal than the number of the previous page.'
        if index < len(array)-1:
            f'Syntax error in "{sintax}". When you use a colon at the end, there cannot be a trailing number.'
        return list(range(int(query[0]), pages_lenght+1, int(query[1])))
    elif re.fullmatch(r'^:\d+:\d+$', sintax):
        # :5:14
        query = sintax.split(':')
        if index != 0:
            return f'Syntax error in "{sintax}". When you use a colon at the beginning there cannot be a previous number.'
        if int(query[-1]) > pages_lenght:
            return f'Syntax error in "{sintax}". The number of the final page cannot be greater than the total number of pages in the file.'
        if index < len(array)-1:
            if array[index+1].isnumeric():
                if int(query[-1]) >= int(array[index+1]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
            else:
                if int(query[-1]) >= int(array[index+1].split(':')[0]):
                    return f'Syntax error in "{sintax}". The number of the final page cannot be greater or equal than the number of the next page.'
        return list(range(1, int(query[-1])+1, int(query[1])))
    elif re.fullmatch(r'^:\d+:$', sintax):
        if index != 0 or len(array) != 1:
            return f'Syntax error in "{sintax}". When a colon is used at the beginning or at the end, there cannot be numbers before or after it.'
        return list(range(1, pages_lenght+1, int(sintax.split(':')[1])))
    else:
        return f'Syntax error in "{sintax}"'


def check_extension_input_file(path: str):
    if not (path.endswith('.pdf') or path.endswith('.PDF')):
        print(f'{Fore.RED}[x] File "{path}" is not a PDF file.\n\tExiting...')
        sys.exit(1)
