# Import commands functions
from modules.controllers.command_join import join as command_join
from modules.controllers.command_split import split as command_split
from modules.controllers.command_metadata import metadata as command_metadata
# Import third-party libraries
import click
from colorama import init

# Initializing colorama for colors in the terminal output
init()

# Group of click
@click.group()
def cli():
    """
    PDFPY is a python command line interface (CLI) tool that uses the PyPDF2 library to manipulate pdf files in a local environment. With this CLI you can:\n
    * Join pdf files\n
    * Split sheets of a pdf file\n
    * Read or write metadata in pdf files\n
    * Add custom watermarks\n
    * Protect pdf files (add or remove passwords)\n
    * Extract text or images from a specific pdf file or sheet\n
    All available documentation is: https://github.com/santiago-rincon/pdfpy\n
    Tool made by: Cristian Santiago Rincón (https://github.com/santiago-rincon)
    """
    pass

# Definition of the join command 
@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', default='merged.pdf', help='Output file path. By default, the file will be saved in the current working directory with the name "merged.pdf". If the output path contains folders that do not exist, they will be created.  Also, if the output path does not contain the extension ".pdf" the file will also be saved as "merged.pdf".', type=click.Path(exists=False))
def join(files, output):
    """
    JOIN DIFFERENT PDF FILES\n
    To join pdf files you must specify the path of the files in order and optionally with the '-o' or '--output' parameter the output path of the final file.\n
    Examples:\n
    [*] The following example merges the pdf files and saves them in the current working folder with the name "merged.pdf". \n
    pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf\n
    [*] The following example joins the pdf files and saves them in the path "new/join.pdf".\n
    pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf -o new/join.pdf\n
    NOTE: the file path can be specified either absolutely or relatively. In addition, the CLI will ignore all paths that do not contain the "pdf " extension. If the output path contains folders that do not exist on the computer, the CLI will create them, and if the output file name is not specified (i.e. the path does not end in ".pdf" extension) it will be saved as "merged.pdf".\n
    All available documentation is: https://github.com/santiago-rincon/pdfpy\n
    Tool made by: Cristian Santiago Rincón (https://github.com/santiago-rincon)
    """
    command_join(files, output)

# Definition of the split command
@cli.command()
@click.argument('file', type=click.Path(exists=True), metavar='PATH_FILE')
@click.argument('pages', metavar='PAGES', required=False)
@click.option('--split-all', '-a', is_flag=True, default=False, help='Separate all sheets of the pdf file. The files will be named page_1, page_2, page_3 ... page_n. If output path is not specified, the files will be saved in the current working directory. If you are going to specify the output path ("-o" or "--output" "parameter) it cannot contain any extensions, only folder names.')
@click.option('--output', '-o', default='splited.pdf', help='Output file path. By default, the file will be saved in the current working directory with the name "splited.pdf". If the output path contains folders that do not exist, they will be created.  Also, if the output path does not contain the extension ".pdf" the file will also be saved as "splited.pdf".', type=click.Path(exists=False))
def split(file, pages, split_all, output):
    """
    SPLIT A PDF FILE\n
    To split pdf files you must specify the path to the main pdf file and specify the pages you want to split as follows:\n
    [*] "2,3,4,5" or "2:5" (splits pages 2 to 5).\n
    [*] "2,5:10,15" (splits page 2, page 5 to 10 and page 15).\n
    [*] "2:2:10" (splits pages 2, 4, 6, 8 and 10).\n
    [*] "1:5:21" (splits pages 1, 6, 11, 16, 21).\n
    [*] "5:" (splits from page 5 to the end of the document)\n
    [*] ":20" (splits from the beginning of the document to page 20)\n
    [*] "1,5:2:10,15" (split pages 1, 5, 7, 9, 15)\n
    [*] ":10,20" (splits from the beginning of the document to page 10 and page 20)\n
    [*] "1,5:" (splits page 1 and from page 5 to the end of the document)\n
    [*] "1,4:2:" (splits page 1 and pages 4, 6, 8, 10 ... to the end of the document)\n
    [*] ":7,10:14" (splits from the beginning of the document to page 7 and pages 10, 11, 12 ... 14)\n
    [*] ":3:" (it is divided from the beginning of the document to the end of the document, skipping from 3 pages at a time. Page 1, 4, 7 ... end of document)\n
    Optionally, with the "-o" or "--output" parameter you can specify the output path of the final file. With the "-a" or "--split-all" parameter you split each page of the file into a new file (page_1 page_2, page_3 ... page_n).\n
    Examples:\n
    [*] The following example splits pages 1 to 10 of the file *"documnet.pdf"* and saves it in the current working directory with the name *splited.pdf* (default name).\n
    pdfpy split document.pdf 1:10\n
    [*] The following example splits page 2, pages 5 to 10 and page 15 of the file *"documnet.pdf"* and saves it in the directory *new_document* with the name *splited.pdf* (default name).\n
    pdfpy split document.pdf 2,5:10,15 -o new_document\n
    [*] The following example splits all pages of the file *"document.pdf"* and saves them in the folder "split_pdf_folder".\n
    pdfpy split document.pdf -a -o split_pdf_folder\n
    NOTE: When the "-a" "--split-all" parameter is used and the output path is not specified, the files will be saved in the current working directory as page_1.pdf, page_2.pdf, page_3.pdf, page_n.pdf. If you are going to specify the output path ("-o" or "--output" parameter) it cannot contain any extensions, only folder names. In addition, when using this parameter it is not necessary to set the number of pages, they will be ignored.\n
    [*] The following example divides every 3 pages from page 5 to page 14 (5, 8, 11, 14)\n
    pdfpy split document.pdf 5:3:14\n
    [*] The following example splits from the beginning of the document to page 40 \n
    pdfpy split document.pdf :40\n
    [*] The following example splits from page 10 to the end of the document\n
    pdfpy split document.pdf 10:
    [*] The following example divides page 1 and 3 and from page 20 to the end of the document\n
    pdfpy split document.pdf 1,3,20:\n
    NOTE: the file path can be specified either absolutely or relatively. In addition, the CLI will ignore all paths that do not contain the "pdf " extension. If the output path contains folders that do not exist on the computer, the CLI will create them, and if the output file name is not specified (i.e. the path does not end in ".pdf" extension) it will be saved as "splited.pdf".\n
    All available documentation is: https://github.com/santiago-rincon/pdfpy\n
    Tool made by: Cristian Santiago Rincón (https://github.com/santiago-rincon)
    """
    command_split(file, pages, split_all, output)

# Definition of the metadata command    
@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file path. By default, the file will be saved in the current working directory with the name "metadata.txt". If the output path contains folders that do not exist, they will be created.  Also, if the output path does not contain the extension ".txt" the file will also be saved as "metadata.txt".', type=click.Path(exists=False))
@click.option('--write-data', '-w', help='Write metadata to a new pdf file from an external file ("json" and "txt" files allowed).', type=click.Path(exists=True))
@click.option('--write', '-W', is_flag=True, default=False, help='Write metadata to a new pdf file indicating the information to the CLI.')
@click.option('--delete', '-d', is_flag=True, default=False, help='Delete metadata of pdf file indicating the information to the CLI.')
def metadata(file, output, write_data, write, delete):
    """
    READ METADATA\n
    To read the metadata from a file you must specify the path to the pdf file and optionally specify an output path ("-o" or "--output") to export the metadata (.txt, .json).\n
    Examples\n
    [*] The following example shows in the console the metadata of the file "example.pdf".\n
    pdfpy metadata example.pdf\n
    [*] The following example exports in the file "metadata.txt" the metadata of the file "example.pdf".\n
    pdfpy metadata example.pdf -o metadata.txt\n
    NOTE: The output file can be ".txt" or ".json". In case it does not contain any of these extensions, it will be changed to ".txt" by default.\n
    WRITE METADATA\n
    To write metadata to a file you must specify the path to the file and with the "-w" or "--write-data" parameter specify the path to a file containing the metadata (the allowed formats are in the "examples folder" of this repository). Or if you want you can specify the "-W" or "-write" parameter so that the CLI will ask you what metadata you want to add. With either option, if you specify the "-o" or "--output" parameter the metadata will be written to a new pdf file (a copy of the source file), otherwise the original file will be overwritten.\n
    Examples:\n
    [*] The following example writes the metadata contained in the "metadata.txt" file to a new file named "file_metadata.pdf".\n
    pdfpy metadata example.pdf -w metadata.txt -o file_metadata.pdf\n
    [*] The following example adds the metadata contained in the file "metadata.json" to the file "file.pdf" (the source file).\n
    pdfpy metadata file.pdf -w metadata.json\n
    [*] The following example will prompt for the metadata to be added and write it to a new file named "new_file.pdf"\n
    pdfpy metadata example.pdf -W -o new_file.pdf\n
    DELETE METADATA\n
    To delete metadata from a file you must specify the file path and the "-d" or "--delete" parameter, the CLI will ask which metadata you want to delete (select with the space key), if you do not select any, all metadata in the file will be deleted (only one called "creator" introduced by PyPDF2 will remain).\n
    pdfpy metadata new_file.pdf -d\n
    All available documentation is: https://github.com/santiago-rincon/pdfpy\n
    Tool made by: Cristian Santiago Rincón (https://github.com/santiago-rincon)
    """
    command_metadata(file, output, write_data, write, delete)

# Initial flow of the program
if __name__ == '__main__':
    # Running the program
    cli()
