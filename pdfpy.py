# Import modules
import modules.commands as commands
# Import third-party libraries
import click
from colorama import init, Fore
# Initializing colorama for colors in the terminal output
init()

# Group of click
@click.group()
def cli():
    """
    PDFPY is a python command line interface (CLI) tool that uses the PyPDF2 library to manipulate pdf files in a local environment. With this CLI you can:\n
    * Join pdf files\n
    * Separate sheets of a pdf file\n
    * Read or write metadata in pdf files\n
    * Add custom watermarks\n
    * Protect pdf files (add or remove passwords)\n
    * Extract text or images from a specific pdf file or sheet\n
    """
    pass


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', default='merged.pdf', help='Output file path. By default, the file will be saved in the current working directory with the name "merged.pdf". If the output path contains folders that do not exist, they will be created.  Also, if the output path does not contain the extension ".pdf" the file will also be saved as "merged.pdf".', type=click.Path(exists=False))
def join(files, output):
    """
    JOIN DIFFERENT PDF FILES\n
    To join pdf files you must specify the path of the files in order and optionally with the '-o' or '--output' parameter the output path of the final file.\n
    Examples:\n
    * The following example merges the pdf files and saves them in the current working folder with the name "merged.pdf". \n
    pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf\n
    * The following example joins the pdf files and saves them in the path "new/join.pdf".\n
    pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf -o new/join.pdf
    """
    commands.join(files, output)

@cli.command()
@click.argument('file', type=click.Path(exists=True), metavar='PATH_FILE')
@click.argument('pages', metavar='PAGES')
@click.option('--split-all', '-a', is_flag=True, default=False, help='Separate all sheets of the pdf file. The files will be named page_1, page_2, page_3 ... page_n. If output path is not specified, the files will be saved in the current working directory. If you are going to specify the output path ("-o" or "--output" "parameter) it cannot contain any extensions, only folder names.')
@click.option('--output', '-o', default='splited.pdf', help='Output file path. By default, the file will be saved in the current working directory with the name "splited.pdf". If the output path contains folders that do not exist, they will be created.  Also, if the output path does not contain the extension ".pdf" the file will also be saved as "splited.pdf".', type=click.Path(exists=False))
def split(file, pages, split_all, output):
    """
    SPLIT A PDF FILE\n
    To split pdf files you must specify the path to the main pdf file and specify the pages you want to split as follows:\n
    * "2,3,4,5" or "2:5" (splits pages 2 to 5).\n
    * "2,5:10,15" (splits page 2, page 5 to 10 and page 15).\n
    * "2:2:10" (splits pages 2, 4, 6, 8 and 10).\n
    * "1:5:21" (splits pages 1, 6, 11, 16, 21).\n
    * "5:" (splits from page 5 to the end of the document)\n
    * ":20" (splits from the beginning of the document to page 20)\n
    Examples:\n
    * The following example splits pages 1 to 10 of the file *"documnet.pdf"* and saves it in the current working directory with the name *splited.pdf* (default name).\n
    pdfpy split document.pdf 1:10\n
    * The following example splits page 2, pages 5 to 10 and page 15 of the file *"documnet.pdf"* and saves it in the directory *new_document* with the name *splited.pdf* (default name).\n
    pdfpy split document.pdf 2,5:10,15 -o new_document\n
    * The following example splits all pages of the file *"document.pdf"* and saves them in the folder "split_pdf_folder".\n
    pdfpy split document.pdf -a -o split_pdf_folder\n
    * The following example divides every 3 pages from page 5 to page 14 (5, 8, 11, 14)\n
    pdfpy split document.pdf 5:3:14\n
    * The following example splits from the beginning of the document to page 40 \n
    pdfpy split document.pdf :40\n
    * The following example splits from page 10 to the end of the document\n
    pdfpy split document.pdf 10:
    * The following example divides page 1 and 3 and from page 20 to the end of the document\n
    pdfpy split document.pdf 1,3,20:
    """
    commands.split(file, pages, split_all, output)
    


# Initial flow of the program
if __name__ == '__main__':
    # Running the program
    cli()