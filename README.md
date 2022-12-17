# PDF Manager tool
#### Video Demo:
#### Description:

PDFs are one of the most popular file formats. We use it A lot in our daily life. 
We sometimes need to modify it by adding, or removing pages, or any other modifications. 
These modifications could be done using some paid software, but this is costly. 
Modifications also could be done online by some websites. But the problem is that these websites are slow,
cannot handle large files, and do not allow an open number of PDFs.

This project is ***PDF manager tool***. It can:

- Remove certain pages.
- Merge multiple files.
- Extract pages from a multi-page file.
- Add a blank page after each page.

---

**Remove pages:**

If you have a large PDF and you are just interested in some pages only.
Select the pages that you want to delete, and the program will delete them, 
and keep the wanted pages. Inputting the pages must be in a specific format:

- Deleting a range of pages:
  - From page `A` to page `H`: `A-H` ; where `H` is included.
  

- Deleting a single page: 
  - Just specify the page; `S` 


- Delete multiple ranges multiple single files, or a set of single pages and ranges:
  - *Just* split the ranges and single pages by a comma. If you want to delete pages `D`, `G`, and from page `X` to `Z`: `D, G, X-Z`

---

**Merge Multiple files:**
This function is useful if you have many related files that are scattered, and you want to send them, print them,
or do something else. The program gets the number of files from the user and then prompts the user to select 
the file from a file dialog. Then it combines the files and outputs the combined file named with the name of the first file.

---

**Extract pages from a multi-paged file:**
So you have a book that you have scanned. You scanned 2 pages per scan. The resulting PDF has 2 book pages each page. 
Then you want to crop each page and get the left and right pages and order them. This will take a long time if it was done manually.
But the program will Do it in seconds or a minute.

You just select the file and select if the original file is left-bound (Like English) or right-bound (Like Arabic).
The program then will crop each page twice, getting the right page, and the left page, it will then store them
in 2 temporary PDF files; one file for the left and the other for the right. Then the program will loop for the number of pages;
- If the book is right-bound; it will add the right page first, then the left page.
- If the book is left-bound; it will add the left page first, then the right page.

Then, temporary files will be deleted and the final file will be outputted.

---
**Add a blank page after each page:**

Suppose you have a file that you need for a lecture. 
You might print it as single-faced, with the page at the front, and the back side is empty to take notes on it. 
But when you will right on the blank page, it won't be neat as lines might be un-straight, and the writing size may differ. 
This function will take the PDF file, and prompts the user to select the added page type:

- Blank: *Just a white blank page.*
- Lined: *A page with 28 lines, has red margin lines on the left and right.*
- Graphed: *A graphed paper with large grids that has small grids in it.*

The program then outputs the file with added sheets after each page.

---
*The program has a textual console UI. Colors are added by `colorama` module for a better user-interface.*

*The program opens a file dialog from `tkinter` module for the user to select the file.*

---
#### Problems that the program could face:

**Only 2 pages of the result PDF are shown, the others are blank:**
> This problem can occur in Adobe Acrobat. It can be avoided by opening the file in Chrome.

**Getting Memory Error**
> The program only accepts files that are less than 50 approximately. it cannot handle large files.