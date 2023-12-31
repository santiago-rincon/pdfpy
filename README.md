# PDFPY
PDFPY is a python command line interface (CLI) tool that uses the [PyPDF2](https://pypdf2.readthedocs.io/en/3.0.0/index.html) library to manipulate pdf files in a local environment. With this CLI you can:
- [Join pdf files](#join-pdf)
- [Separate sheets of a pdf file](#split-pdf-sheets)
- [Read or write metadata in pdf files](#read-and-write-metadata)
- [Add custom watermarks](add-watermark)
- [Protect pdf files](#add-and-remove-passwords)
- [Extract text or images from a specific pdf file or sheet](#extract-text-and-images)
## Installation 
To install the CLI you must:
1. Clone the repository
```bash
git clone https://github.com/santiago-rincon/pdfpy.git
cd pdfpy
```
2. Install the required dependencies
```bash
pip install -r requirements.txt
```
## Usage
### Split pdf sheets
To split pdf files you must specify the path to the main pdf file and specify the pages you want to split as follows:
- `2,3,4,5` or `2:5` (splits pages 2 to 5).
- `2,5:10,15` (splits page 2, page 5 to 10 and page 15).
- `2:2:10` (splits pages 2, 4, 6, 8 and 10)
- `1:5:21` (splits pages 1, 6, 11, 16, 21)
- `5:` (splits from page 5 to the end of the document)
- `:20` (splits from the beginning of the document to page 20)
- `1,5:2:10,15` (split pages 1, 5, 7, 9, 15)
- `:10,20` (splits from the beginning of the document to page 10 and page 20)
- `1,5:` (splits page 1 and from page 5 to the end of the document)
- `1,4:2:` (splits page 1 and pages 4, 6, 8, 10 ... to the end of the document)
- `:7,10:14` (splits from the beginning of the document to page 7 and pages 10, 11, 12 ... 14)
- `:3:` (it is divided from the beginning of the document to the end of the document, skipping from 3 pages at a time. Page 1, 4, 7 ... end of document)

Optionally, with the `-o` or `--output` parameter you can specify the output path of the final file.
With the `-a` or `--split-all` parameter you split each page of the file into a new file (page_1 page_2, page_3 ... page_n).
#### Examples:
- The following example splits pages 1 to 10 of the file *"documnet.pdf"* and saves it in the current working directory with the name *splited.pdf* (default name).
```python
pdfpy split document.pdf 1:10
```
- The following example splits page 2, pages 5 to 10 and page 15 of the file *"documnet.pdf"* and saves it in the directory *new_document* with the name *splited.pdf* (default name).
```python
pdfpy split document.pdf 2,5:10,15 -o new_document
```
- The following example splits all pages of the file *"document.pdf"* and saves them in the folder *"split_pdf_folder"*.
```python
pdfpy split document.pdf -a -o split_pdf_folder
```
***NOTE:*** When the `-a` `--split-all` parameter is used and the output path is not specified, the files will be saved in the current working directory as page_1.pdf, page_2.pdf, page_3.pdf, page_n.pdf. If you are going to specify the output path (`-o` or `--output` parameter) it cannot contain any extensions, only folder names. In addition, when using this parameter it is not necessary to set the number of pages, they will be ignored.
- The following example divides every 3 pages from page 5 to page 14 (5, 8, 11, 14)
```python
pdfpy split document.pdf 5:3:15
```
- The following example splits from the beginning of the document to page 40 
```python
pdfpy split document.pdf :40
```
- The following example splits from page 10 to the end of the document
```python
pdfpy split document.pdf 10:
```
- The following example divides page 1 and 3 and from page 20 to the end of the document
```python
pdfpy split document.pdf 1,3,20:
```
***NOTE:*** the file path can be specified either absolutely or relatively. In addition, the CLI will **ignore** all paths that **do not contain** the ***"pdf "*** extension. If the output path contains folders that do not exist on the computer, the CLI will create them, and if the output file name is not specified (i.e. the path does not end in ".pdf" extension) it will be saved as "splited.pdf".
### Join pdf
To join pdf files you must specify the path of the files in order and optionally with the `-o` o `--output` parameter the output path of the final file.
#### Examples:
- The following example merges the pdf files and saves them in the current working folder with the name "merged.pdf". 
```python
pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf
```
- The following example joins the pdf files and saves them in the path "new/join.pdf". 
```python
pdfpy join file_1.pdf file_2.pdf file_3.pdf...file_n.pdf -o new/join.pdf
```
***NOTE:*** the file path can be specified either absolutely or relatively. In addition, the CLI will **ignore** all paths that **do not contain** the ***"pdf "*** extension. If the output path contains folders that do not exist on the computer, the CLI will create them, and if the output file name is not specified (i.e. the path does not end in ".pdf" extension) it will be saved as "merged.pdf".
### Read and write metadata
#### Read metadata
To read the metadata from a file you must specify the path to the pdf file and optionally specify an output path (`-o` or `--output`) to export the metadata (.txt, .json).
##### Examples
- The following example shows in the console the metadata of the file *"example.pdf"*.
```python
pdfpy metadata example.pdf
```
- The following example exports in the file "metadata.txt" the metadata of the file "example.pdf".
```python
pdfpy metadata example.pdf -o metadata.txt
```
***NOTE:*** the output file can be *".txt"* or *".json"*. In case it does not contain any of these extensions, it will be changed to *".txt"* by default.
#### Write metadata
To write metadata to a file you must specify the path to the file and with the `-w` or `--write-data` parameter specify the path to a file containing the metadata (the allowed formats are in the *"examples folder"* of this repository). Or if you want you can specify the `-W` or `-write` parameter so that the CLI will ask you what metadata you want to add. With either option, if you specify the `-o` or `--output` parameter the metadata will be written to a new pdf file (a copy of the source file), otherwise the original file will be overwritten.
##### Examples:
- The following example writes the metadata contained in the *"metadata.txt"* file to a new file named *"file_metadata.pdf"*.
```python
pdfpy metadata example.pdf -w metadata.txt -o file_metadata.pdf
```
- The following example adds the metadata contained in the file "metadata.json" to the file "file.pdf" (the source file).
```python
pdfpy metadata file.pdf -w metadata.json
```
- The following example will prompt for the metadata to be added (as shown in the following image) and write it to a new file named "new_file.pdf"
```python
pdfpy metadata example.pdf -W -o new_file.pdf
```

![Write metadata](assets/write_metadata.png)
##### Delete metadata
To delete metadata from a file you must specify the file path and the `-d` or `--delete` parameter, the CLI will ask which metadata you want to delete (select with the space key), if you do not select any, all metadata in the file will be deleted (only one called "creator" introduced by PyPDF2 will remain).
##### Examples:
- The following example removes the metadata "Keywords", "Author" and "Title" from the file "new_file.pdf".
```python
pdfpy metadata new_file.pdf -d
```
![Delete metadata](assets/delete_metadata.png)
- The following example removes all metadata from the file "new_file.pdf".
![Delete all metadata](assets/delete_all_metadata.png)
### Add watermark

### Add and remove password
To encrypt or decrypt a file you must specify the path to the pdf **file**, the **mode** (encrypt or decrypt), the **password** (if it has spaces it must be enclosed in single quotation marks) and optionally specify an **output path** ("-o" or "--output") to export the file decrypted.

```shell
pdfpy crypt <FILE> <MODE> <PASSWORD> -o <OUTPUT_PATH>
```
#### Examples:
- The following example encrypt file "example.pdf" with the password "test" and save in the current working directory.
```python
pdfpy crypt example.pdf encrypt test
```
- The following example decrypt file "example.pdf" with the password "test" and save in the current working directory.
```python
pdfpy crypt example.pdf decrypt test
```
- The following example encrypt file "example.pdf" with the password "spaces in the password" and save in a new file named "encrypted_example.pdf".
```python
pdfpy crypt example.pdf encrypt 'spaces in the password' -o encrypted_example.pdf
```
***NOTE:*** the file path can be specified either absolutely or relatively. In addition, the CLI will **ignore** all paths that **do not contain** the ***"pdf "*** extension. If the output path contains folders that do not exist on the computer, the CLI will create them, and if the output file name is not specified (i.e. the path does not end in ".pdf" extension) it will be saved as "merged.pdf".
### Extract text and images

## Note for Windows
If you want to add the script to the PATH in windows you must add the text string ".py" to the `PATHEXT` environment variable.

```powershell
$env:PATHEXT += ";.py"
```

