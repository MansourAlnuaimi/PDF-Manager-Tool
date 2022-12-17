import os
import re
import sys
import colorama
import tkinter as tk
from tkinter import filedialog as fd
from PyPDF2 import PdfWriter, PdfReader


def main():
    # Main menu
    colorama.init(autoreset=True)
    print('\n' + RED +
          '╔═╗╔╦═╗╔═╗ \n' +
          '╠═╝ ║ ║╠═      \n' +
          '╩  ═╩═╝╚   \n' + BLU +
          '┌┬┐┌─┐┌┐┌┌─┐┌─┐┌─┐┬─┐ \n' +
          '│││├─┤│││├─┤│ ┬├┤ ├┬┘ \n' +
          '┴ ┴┴ ┴┘└┘┴ ┴└─┘└─┘┴└─ ')

    print(BLU + '══' * 20)
    print('\n\x1B[3mSelect an option:\n' + MGN +
          ' 1) Delete pages \n' +
          ' 2) Merge multiple PDFs \n' +
          ' 3) Extract pages from multi-paged PDF file \n' +
          ' 4) Add new pages after each page ')
    option = input(YLW + '\nOption: ')

    # If the option was invalid
    while option not in ['1', '2', '3', '4']:
        print(ERR + 'Invalid option.')
        option = input(YLW + '\nOption: ')

    match option:
        case '1':
            delete_pages()
        case '2':
            merge()
        case '3':
            crop()
        case '4':
            add_pages()


def delete_pages():
    # Open the file
    filename = get_file()
    # if the file is not PDF
    if not ispdf(filename): sys.exit(ERR + 'File is not a pdf.')

    # Extract the file's name from the path
    name = get_file_name(filename)
    print(CYN + f'\nFile:', name)
    # Instructions
    pages_to_delete = input(BLU + '--' * 20 + MGN +
                            '\n- Use a dash `-` to specify a range.' +
                            '\n- Use a number to specify a single page.' +
                            '\n- Separate pages and ranges by a comma. \n' +
                            YLW + '\nPages to remove: ')
    pages = []  # store the pages to delete
    pages_to_delete = pages_to_delete.split(',')

    for pg in pages_to_delete:
        pg = pg.strip()

        # if the item is a single page
        if match := re.search(r'^(\d+)', pg) and '-' not in pg:
            pages.append(int(pg))
        # if the item is a range
        elif match := re.search(r'(\d+)-(\d+)', pg):
            start = int(match.group(1))
            end = int(match.group(2)) + 1
            # add the pages to the list
            for i in range(start, end): pages.append(i)

    # subtract 1 from the page numbers for 0 indexing
    pages = subtract1(pages)

    infile = PdfReader(filename, "rb")
    output = PdfWriter()

    # add the page only if it isn't in the `pages` list
    for i in range(len(infile.pages)):
        if i not in pages:
            p = infile.getPage(i)
            output.add_page(p)

    # remove .pdf from the filename
    filename = remove_suffix(filename)
    saved = f'{filename}_removedPages.pdf'
    with open(saved, 'wb') as f:
        output.write(f)
    # open the file in a window after saving
    os.system('start ' + saved)


def merge():
    # get how many files to merge
    num = int(input(YLW + 'Number of files to merge: '))
    files = []
    for n in range(num):
        file = get_file(n+1)
        files.append(file)

    output = PdfWriter()
    # for each file
    for file in files:
        # if the file is not pdf
        if not ispdf(file):
            sys.exit(ERR + 'File is not a pdf.')

        infile = PdfReader(file, 'rb')
        # add the file's pages to the output file for each file
        for pg in range(len(infile.pages)):
            p = infile.getPage(pg)
            output.add_page(p)

    # remove .pdf from the first file's name
    name = remove_suffix(files[0])
    # output the file
    saved = f'{name}_merged.pdf'
    with open(saved, 'wb') as f:
        output.write(f)

    # open the file in a window after saving
    os.system('start ' + saved)


def crop():
    # get file
    filename = get_file()
    # if the file is not pdf
    if not ispdf(filename):
        sys.exit(ERR + 'File is not a pdf.')

    # Extract the file's name from the path
    name = get_file_name(filename)
    print(CYN + f'\nFile:', f'{name}\n')

    binding = input(YLW + "Book's binding: (R|L): ").upper()
    while binding not in ['R', 'L']:
        print(ERR + 'Invalid option.')
        binding = input(YLW + "Side of binding: (R|L): ").upper()

    match binding:
        case 'R':
            right(filename)
        case 'L':
            left(filename)


def right(file):
    # open the file 2 times, one for the front (right) side, one for the back (left) side
    infile1 = PdfReader(file, 'rb')
    infile2 = PdfReader(file, 'rb')
    # initialize the right (front), left (back) files, and the final outputted file
    right_pg = PdfWriter()
    left_pg = PdfWriter()
    output = PdfWriter()
    # get number of pages
    pages = infile1.getNumPages()
    # front side
    for page in range(pages):
        # get dimensions
        p = infile1.getPage(page)
        pg_height = p.cropbox.getUpperLeft()[1]
        pg_width = p.cropbox.getUpperRight()[0]
        # crop the page to the half to select the right page
        '''
        Dimensions' guide:
        .------------------------------------.
        | (0, height)       (width, height)  |
        |                                    |
        | (0, 0)                (width, 0)   |
        |____________________________________|
        '''
        p.cropbox.setLowerLeft((pg_width / 2, 0))
        p.cropbox.setUpperRight((pg_width, pg_height))
        # add the page
        right_pg.add_page(p)

    for page in range(pages):
        # get the dimensions
        p = infile2.getPage(page)
        pg_height = p.cropbox.getUpperLeft()[1]
        pg_width = p.cropbox.getUpperRight()[0]
        # crop the page to the half to select the left page
        p.cropbox.setLowerLeft((0, pg_height))
        p.cropbox.setUpperRight((pg_width / 2, 0))
        # add the page
        left_pg.add_page(p)

    # output 2 temporary files
    filename = remove_suffix(file)
    with open(f'{filename}_RIGHT.pdf', 'wb') as f:
        right_pg.write(f)
    with open(f'{filename}_LEFT.pdf', 'wb') as f:
        left_pg.write(f)
    try:
        # add the pages in the proper order.
        for n in range(pages):
            # front page
            file1 = PdfReader(f'{filename}_RIGHT.pdf', 'rb')
            pg1 = file1.getPage(n)
            output.add_page(pg1)
            # back page
            file2 = PdfReader(f'{filename}_LEFT.pdf', 'rb')
            pg2 = file2.getPage(n)
            output.add_page(pg2)
    except MemoryError:  # Program will raise MemoryError if the file was very large
        # remove temporary files
        os.remove(f'{filename}_RIGHT.pdf')
        os.remove(f'{filename}_LEFT.pdf')
        sys.exit(RED + 'MemoryError:\n' + ERR + 'The file is very large. Program cannot extract its pages.')
    else:
        # finally, output the file and open it
        with open(f'{filename}_formatted.pdf', 'wb') as f:
            output.write(f)
        os.system('start ' + f'{filename}_formatted.pdf')
        # remove temporary files
        os.remove(f'{filename}_RIGHT.pdf')
        os.remove(f'{filename}_LEFT.pdf')


def left(file):
    # open the file 2 times, one for the front (left) side, one for the back (right) side
    infile1 = PdfReader(file, 'rb')
    infile2 = PdfReader(file, 'rb')
    # initialize the left (front), right (back) files, and the final outputted file
    left_pg = PdfWriter()
    right_pg = PdfWriter()
    output = PdfWriter()
    # get number of pages
    pages = infile1.getNumPages()
    # front side
    for page in range(pages):
        # get the page's dimensions
        p = infile1.getPage(page)
        pg_height = p.cropbox.getUpperLeft()[1]
        pg_width = p.cropbox.getUpperRight()[0]
        # Set the left (front) page
        p.cropbox.setLowerRight((pg_width / 2, 0))
        p.cropbox.setUpperLeft((0, pg_height))
        left_pg.add_page(p)

    for page in range(pages):
        # get the page's dimensions
        p = infile2.getPage(page)
        pg_height = p.cropbox.getUpperLeft()[1]
        pg_width = p.cropbox.getUpperRight()[0]
        # Set the right (back) page
        p.cropbox.setLowerLeft((pg_width / 2, 0))
        p.cropbox.setUpperRight((pg_width, pg_height))
        right_pg.add_page(p)

    # output the 2 temporary files
    filename = remove_suffix(file)
    with open(f'{filename}_LEFT.pdf', 'wb') as f:
        left_pg.write(f)
    with open(f'{filename}_RIGHT.pdf', 'wb') as f:
        right_pg.write(f)

    try:
        # add the pages in the proper order.
        for n in range(pages):
            # front page
            file1 = PdfReader(f'{filename}_LEFT.pdf', 'rb')
            pg1 = file1.getPage(n)
            output.add_page(pg1)
            # back page
            file2 = PdfReader(f'{filename}_RIGHT.pdf', 'rb')
            pg2 = file2.getPage(n)
            output.add_page(pg2)
    except MemoryError:
        # remove temporary files
        os.remove(f'{filename}_RIGHT.pdf')
        os.remove(f'{filename}_LEFT.pdf')
        sys.exit(RED + 'MemoryError:\n' + ERR + 'The file is very large. Program cannot extract its pages.')
    else:
        # finally, output the file and open it
        with open(f'{filename}_formatted.pdf', 'wb') as f:
            output.write(f)
        os.system('start ' + f'{filename}_formatted.pdf')
        # remove temporary files
        os.remove(f'{filename}_LEFT.pdf')
        os.remove(f'{filename}_RIGHT.pdf')


def add_pages():
    # get the file & read it
    filename = get_file()
    # if the file is not pdf
    if not ispdf(filename):
        sys.exit(ERR + 'File is not a pdf.')

    # Extract the file's name from the path
    name = get_file_name(filename)
    print(CYN + '\nFile:', name)
    print(BLU + '--' * 20)
    infile = PdfReader(filename, "rb")
    # initialize the output file
    output = PdfWriter()
    # Select the type of the added sheet
    pg_type = input('Type of empty page: \n' + MGN +
                    ' 1) Blank. \n' +
                    ' 2) Lined. \n' +
                    ' 3) Graph paper. \n' +
                    YLW + 'Option: ')
    # If the user typed an invalid option
    while pg_type not in ['1', '2', '3']:
        print(ERR + 'Enter a valid option.')
        pg_type = input(YLW + 'Option: ')

    match pg_type:
        case '1':
            page = r'pages\blank.pdf'
        case '2':
            page = r'pages\lined.pdf'
        case '3':
            page = r'pages\graph.pdf'
        case _:
            sys.exit()

    # get the wanted type sheet
    new_page = PdfReader(page, 'rb')
    new = new_page.getPage(0)

    # add new page after each page
    for i in range(len(infile.pages)):
        p = infile.getPage(i)
        # file's page
        output.add_page(p)
        # new sheet
        output.add_page(new)

    # remove .pdf from the filename
    filename = remove_suffix(filename)
    saved = f'{filename}_pageAdded.pdf'
    with open(saved, 'wb') as f:
        output.write(f)
    # open the file in a window after saving
    os.system('start ' + saved)


def ispdf(filename):
    if filename.endswith('.pdf'):
        return True
    else:
        return False

def subtract1(ls):
    # Subtracts 1 from a list to match 0 indexing
    return [i - 1 for i in ls]

def remove_suffix(path):
    # Removes `.pdf` from file's name for a clean file name
    if path.endswith('.pdf'):
        return path.replace('.pdf', '')
    else:
        return path

def get_file(*n):
    # gets the file from a GUI dialog, returns its path
    root = tk.Tk()
    root.attributes('-alpha', 0.0)
    root.attributes('-topmost', True)

    if n == (): n = ''
    else: n = n[0]
    filename = fd.askopenfilename(parent=root, title=f'Select file ' + str(n))
    root.destroy()
    return filename

def get_file_name(filename):
    # Extract the file's name from the path
    name = filename.split('\\')[-1]
    name = filename.split('/')[-1]
    return name

# colorama colors
RED = colorama.Fore.RED
GRN = colorama.Fore.GREEN
BLU = colorama.Fore.BLUE
CYN = colorama.Fore.CYAN
MGN = colorama.Fore.MAGENTA
YLW = colorama.Fore.YELLOW  # used for inputs
ERR = colorama.Fore.BLACK + colorama.Back.RED   # used for errors

if __name__ == '__main__':
    main()