# Import standard libraries
from datetime import datetime
import os, sys, re, json

# Import local modules
import modules.utilities as utilities

# Import third-party libraries
from colorama import Fore
from PyPDF2 import PdfWriter, PdfReader
import inquirer


def metadata(file, output, write_data, write):
    file = os.path.abspath(file)
    # Check if the input file contains the extension ".pdf"
    if not file.endswith('.pdf'):
        print(f'{Fore.RED}[x] File "{file}" is not a PDF file.\n\tExiting...')
        sys.exit(1)
    reader = PdfReader(file)
    metadata = reader.metadata
    dict_metadata = json.loads(json.dumps(metadata))
    # Case: -o X -w X
    if not output and not write_data and not write:
        print(f'{Fore.GREEN}[+] Metadata:')
        for key, value in dict_metadata.items():
            key = key.replace('/', '')
            if re.fullmatch(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\+\d{2}'\d{2}')?", value):
                value = datetime.strptime(value[2:14], '%Y%m%d%H%M%S')
            print(f'\t{Fore.LIGHTBLUE_EX}{key}: {value}')
    # Case: -o Path -w X
    elif output and not write_data and not write:
        output = os.path.abspath(output)
        if not os.path.splitext(output)[1]:
            if not os.path.exists(output):
                os.makedirs(output)
            output = os.path.join(output, 'metadata.txt')
        else:
            utilities.create_folders(output)
            if os.path.splitext(output)[1] != '.txt' and os.path.splitext(output)[1] != '.json':
                print(
                    f'{Fore.YELLOW}[!] The output file extension was changed to ".txt". You can too use "json" extension to save the metadata in a json file.')
                output = os.path.splitext(output)[0] + '.txt'
        utilities.output_file_exist(output, 'metadata')
        with open(output, 'w') as f:
            if os.path.splitext(output)[1] != '.json':
                f.write("Metadata:\n")
                for key, value in dict_metadata.items():
                    key = key.replace('/', '')
                    if re.fullmatch(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\+\d{2}'\d{2}')?", value):
                        value = datetime.strptime(value[2:14], '%Y%m%d%H%M%S')
                    f.write(f'\t{key}: {value}\n')
            else:
                array = []
                for key, value in dict_metadata.items():
                    key = key.replace('/', '')
                    if re.fullmatch(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\+\d{2}'\d{2}')?", value):
                        value = datetime.strptime(value[2:14], '%Y%m%d%H%M%S')
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    array.append(tuple([key, value]))
                f.write(json.dumps(dict(array), indent=4))
        print(f'{Fore.GREEN}[+] Metadata saved successfully in:\n{output}')
    # Case: -o Path -W
    elif output and not write_data and write:
        output = os.path.abspath(output)
        if not os.path.splitext(output)[1]:
            if not os.path.exists(output):
                os.makedirs(output)
            file_name = os.path.split(file)
            file_name = os.path.splitext(file_name[1])[0]
            file_name += '_metadata.pdf'
            output = os.path.join(output, file_name)
        else:
            utilities.create_folders(output)
            if os.path.splitext(output)[1] != '.pdf':
                print(
                    f'{Fore.YELLOW}[!] The output file extension was changed to ".pdf".')
                output = os.path.splitext(output)[0] + '.pdf'
        utilities.output_file_exist(output, 'metadata')
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # Create dictionary to write metadata
        continue_write = True
        dict_write = {}
        while continue_write:
            questions = [
                inquirer.Text("key", message='Type the metadata key'),
                inquirer.Text("value", message='Type the value for "{key}"'),
                inquirer.Confirm(
                    "continue_write", message='Do you want to add another metadata?')
            ]
            answers = inquirer.prompt(questions)
            if (answers['key'] == '' or answers['value'] == '') and not bool(dict_write) and answers['continue_write']:
                print(f'{Fore.RED}[!] The key or value cannot be empty.')
            elif (answers['key'] == '' or answers['value'] == '') and not bool(dict_write) and not answers['continue_write']:
                break
            elif (answers['key'] == '' or answers['value'] == '') and bool(dict_write) and answers['continue_write']:
                print(
                    f'{Fore.YELLOW}[!] Remember that the key or value cannot be empty.')
            elif (answers['key'] == '' or answers['value'] == '') and bool(dict_write) and not answers['continue_write']:
                print(
                    f'{Fore.YELLOW}[!] The key or value cannot be empty.\n\tWriting the previously added metadata.')
                break
            else:
                dict_write['/'+answers['key']] = answers['value']
                continue_write = answers['continue_write']
        # Add metadata
        if bool(dict_write):
            writer.add_metadata(metadata)
            writer.add_metadata(dict_write)
        else:
            writer.add_metadata({})
            print(
                f'{Fore.YELLOW}[!] Relevant metadata of the file was deleted.')
        # Write new file
        with open(output, 'wb') as out:
            writer.write(out)
        print(f'{Fore.GREEN}[+] File saved in:\n{output}')
