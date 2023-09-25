# Import standard libraries
from datetime import datetime
import os, sys, re, json

# Import local modules
import modules.utilities as utilities

# Import third-party libraries
from colorama import Fore
from PyPDF2 import PdfWriter, PdfReader
import inquirer


def metadata(file, output, write_data, write, delete):
    # Convert input file to absolute path
    file = os.path.abspath(file)
    # Check if the input file contains the extension ".pdf"
    utilities.check_extension_input_file(file)
    reader = PdfReader(file)
    metadata = reader.metadata
    dict_metadata = json.loads(json.dumps(metadata))
    # Case: 0 0 0 0
    if not output and not write_data and not write and not delete:
        _ignore_delete(delete)
        print(f'{Fore.GREEN}[+] Metadata:')
        for key, value in dict_metadata.items():
            key,value = _formatting_metadata(key, value)
            print(f'\t{Fore.LIGHTBLUE_EX}{key}: {value}')
    # Case: 1 0 0 x
    elif output and not write_data and not write:
        _ignore_delete(delete)
        output = _check_output_file_path(file, output, False)
        utilities.output_file_exist(output, 'metadata')
        with open(output, 'w') as f:
            if os.path.splitext(output)[1] != '.json':
                f.write("Metadata:\n")
                for key, value in dict_metadata.items():
                    key,value = _formatting_metadata(key, value)
                    f.write(f'\t{key}: {value}\n')
            else:
                array = []
                for key, value in dict_metadata.items():
                    array.append(_formatting_metadata(key, value, True))
                f.write(json.dumps(dict(array), indent=4))
        print(f'{Fore.GREEN}[+] Metadata saved successfully in:\n{output}')
    # Case: 1 0 1 x
    elif output and not write_data and write:
        _ignore_delete(delete)
        output = _check_output_file_path(file, output)
        utilities.output_file_exist(output, 'metadata')
        # Create copy of file
        writer = _create_copy_file_input(reader.pages)
        # Create dictionary to write metadata
        dict_write = _metadata_inquirer()
        # Add metadata
        writer = _add_metadata(writer, dict_write, metadata)
        # Write new file
        _write_metadata(output, writer)
    # Case: 0 0 1 x
    elif not output and not write_data and write:
        _ignore_delete(delete)
        # Create copy of file
        writer = _create_copy_file_input(reader.pages)
        # Create dictionary to write metadata
        dict_write = _metadata_inquirer()
        # Add metadata
        writer = _add_metadata(writer, dict_write, metadata)
        # Write in the same file
        _write_metadata(file, writer)
    # Case: x 1 1 x
    elif write_data and write:
        print(f'{Fore.RED}[x] Parameters "-write" and "--write-data" can not be join. For more information to use try:\n\t{Fore.LIGHTMAGENTA_EX}pdfpy metadata --help\n\tExiting...')
        sys.exit(1)
    # Case: 0 1 0 x
    elif not output and write_data and not write:
        _ignore_delete(delete)
        # Create copy of file
        writer = _create_copy_file_input(reader.pages)
        # Check metadata file input
        write_data = _check_write_data_path(write_data)
        # Build dictionary with metadata
        dictionary_metadata = _file_to_dictionary(write_data)
        # Add metadata to the writer
        writer = _add_metadata(writer, dictionary_metadata, metadata)
        # Write in the same file
        _write_metadata(file, writer)
    # Case: 1 1 0 x
    elif output and write_data and not write:
        _ignore_delete(delete)
        output = _check_output_file_path(file, output)
        utilities.output_file_exist(output, 'metadata')
        # Create copy of file
        writer = _create_copy_file_input(reader.pages)
        # Check metadata file input
        write_data = _check_write_data_path(write_data)
        # Build dictionary with metadata
        dictionary_metadata = _file_to_dictionary(write_data)
        # Add metadata to the writer
        writer = _add_metadata(writer, dictionary_metadata, metadata)
        # Write new file
        _write_metadata(output, writer)
    # Case: 0 0 0 1
    elif not output and not write_data and not write and delete:
        # Create copy of file
        writer = _create_copy_file_input(reader.pages)
        # Selection of metadata to delete
        answers = _select_metadata_to_delete(dict_metadata)
        # Delete metadata
        _delete_metadada(answers, dict_metadata, metadata, writer, file)

def _metadata_inquirer():
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
    return dict_write

def _ignore_delete(delete : bool):
    if delete:
        print(f'{Fore.YELLOW}[!] Parameter "--delete" or "-d" will be ignore. For more information to use try:\n\t{Fore.LIGHTMAGENTA_EX} pdfpy metadata --help\n')

def _check_output_file_path(file, path, same_name_input=True):
    output = os.path.abspath(path)
    if not os.path.splitext(output)[1]:
        if not os.path.exists(output):
            os.makedirs(output)
        if same_name_input:
            file_name = os.path.split(file)[1]
            file_name = os.path.splitext(file_name)[0]
            file_name += '_metadata.pdf'
        else:
            file_name = "metadata.txt"
        return os.path.join(output, file_name)
    else:
        utilities.create_folders(output)
        if os.path.splitext(output)[1] != '.pdf' and same_name_input:
            print(f'{Fore.YELLOW}[!] The output file extension was changed to ".pdf".')
            return os.path.splitext(output)[0] + '.pdf'
        elif os.path.splitext(output)[1] != '.txt' and os.path.splitext(output)[1] != '.json' and not same_name_input:
            print(f'{Fore.YELLOW}[!] The output file extension was changed to ".txt". You can too use "json" extension to save the metadata in a json file.')
            return os.path.splitext(output)[0] + '.txt'
        else:
            return output

def _check_write_data_path(path):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        print(f'{Fore.RED}[x] You must specify a file to extract the metadata, not a folder.\n\tExiting...')
        sys.exit(1)
    return path

def _file_to_dictionary(file):
    if os.path.splitext(file)[1] == '.json':
        with open(file, 'r') as f:
            try:
                temp_data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f'{Fore.RED}[x] The file "{file}" is not a valid JSON.\n\tExiting...')
                sys.exit(1)
        data = {}
        for key, value in temp_data.items():
            if not isinstance(value, (str, int, float)):
                print(f'{Fore.RED}[x] The file "{file}" is not a valid JSON.\n{Fore.YELLOW}[!] Values can be numbers or text only.\n{Fore.RED}[x]Error in: {Fore.MAGENTA}"{key}": {value}\n\t{Fore.RED}Exiting...')
                sys.exit(1)
            data['/'+key] = value.strip() if isinstance(value, str) else str(value)
        return data
    else:
        f = open(file,'r')
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(f'{Fore.RED}[x] The file "{file}" is not UTF-8 encoded.\n\tExiting...')
            sys.exit(1)
        len_lines = len(lines)
        if len_lines == 1:
            _check_format(lines, file)
            lines = lines[0].split(';')
            return _create_dict(lines, ',')
        elif len_lines > 1:
            _check_format(lines, file)
            if lines[0].find(',') != -1:
                separator = ','
            else:
                separator = '\t'
            return _create_dict(lines, separator)
        else:
            print(f'{Fore.RED}[x] The file "{file}" is empty.\n\tExiting...')

def _check_format(lines, file):
    regexs = [r'(.*)\t(.*)\n?', r'(.*),([^;]+)\n?']
    for line in lines:
        for regex in regexs:
            checked = False
            if re.fullmatch(regex, line):
                checked = True

                break
        if not checked:
            print(f'{Fore.RED}[x] The file "{file}" is not in the correct format.\n\tExiting...')
            sys.exit(1)   

def _create_dict(lines, separator:str):
    dict = {}
    for line in lines:
        metadata = line.split(separator)
        dict['/' + metadata[0].strip()] = metadata[1].strip()
    return dict

def _create_copy_file_input(reader):
    writer = PdfWriter()
    for page in reader:
        writer.add_page(page)
    return writer

def _add_metadata(writer, dictionary_metadata, metadata, delete=False):
    # Add metadata
    if bool(dictionary_metadata):
        if not delete:
            writer.add_metadata(metadata)
        writer.add_metadata(dictionary_metadata)
    else:
        writer.add_metadata({})
        print(f'{Fore.YELLOW}[!] Relevant metadata of the file was deleted.')
    return writer

def _write_metadata(file, writer):
    with open(file, 'wb') as out:
            writer.write(out)
            print(f'{Fore.GREEN}[+] File saved in:\n{file}')

def _formatting_metadata(key:str, value:str, json_file=False):
    key = key.replace('/', '')
    isdate = re.fullmatch(r'D:(\d{14})(\-?\+?)(\d{2}\'\d{2}\')', value)
    if  isdate and not json_file:
        value = datetime.strptime(value[2:14], '%Y%m%d%H%M%S')
    elif isdate and json_file:
        value = datetime.strptime(value[2:14], '%Y%m%d%H%M%S')
        value = value.strftime('%Y-%m-%d %H:%M:%S')
    return (key, value)

def _delete_metadada(answers, dict_metadata, metadata, writer, file ):
    if len(answers) > 0:
        for answer in answers:
            del dict_metadata['/'+answer.split(':')[0]]
        writer = _add_metadata(writer, dict_metadata, metadata, delete=True)
        _write_metadata(file, writer)
    else:
        writer = _add_metadata(writer, {}, metadata, delete=True)
        _write_metadata(file, writer)

def _select_metadata_to_delete(dict_metadata):
    choises = []
    for key, value in dict_metadata.items():
        key,value = _formatting_metadata(key, value)
        choises.append(f'{key}: {value}')
    questions = [inquirer.Checkbox('metadata_to_delete',message='What metadata would you want to delete?', choices=choises)]
    print(f'{Fore.YELLOW}[!] Select the metadata to be deleted with the "space key" or press the "enter key" without selecting anything to delete all metadata.')
    return inquirer.prompt(questions)['metadata_to_delete']
