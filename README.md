# PDF Toolkit (Console-Based Python Project)

PDF Toolkit is a **console-based Python application** that performs three tasks on PDF files:

1. **Merge** - combine several PDF files into a single PDF
2. **Split** - break a PDF apart (one file per page, or a custom page range)
3. **PDF to Text** - extract the text inside a PDF and save it as a `.txt` file

"Console-based" means there are no windows or buttons. The program runs in the terminal, shows a menu, and the user types their answers.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup (first time)](#setup-first-time)
4. [How to run the program](#how-to-run-the-program)
5. [How to use each option](#how-to-use-each-option)
6. [Project structure](#project-structure)
7. [How the code works](#how-the-code-works)
8. [Program flow](#program-flow)
9. [Common errors and fixes](#common-errors-and-fixes)
10. [Limitations](#limitations)
11. [Future improvements](#future-improvements)
12. [Authors](#authors)

---

## Features

- Simple menu-driven interface
- Invalid input does not crash the program; it asks again
- Merge: joins two or more PDFs into one
- Split: one PDF per page, or a custom page range
- Text extraction: text of every page, labelled with page numbers
- After each task the menu returns, until the user chooses Exit

---

## Requirements

| Item | Details |
|------|---------|
| Python | 3.8 or newer |
| pypdf | Reading, merging and splitting PDFs |
| pdfplumber | Extracting text from PDFs |

To check whether Python is installed, run this in the terminal:

```
python --version
```

---

## Setup (first time)

**Step 1:** Download this repository (green **Code** button on GitHub, then **Download ZIP**, then extract the ZIP).

**Step 2:** Open the folder in VS Code (**File > Open Folder**).

**Step 3:** Open a terminal in VS Code (**Terminal > New Terminal**) and install the libraries:

```
pip install pypdf pdfplumber
```

This needs to be done only once. After installing, pip may sometimes print a "dependency conflict" warning. That is only a warning. If the output says the install was successful, you can continue.

---

## How to run the program

In the terminal, inside the folder that contains `pdf_toolkit.py`:

```
python pdf_toolkit.py
```

If `python` does not work, try:

```
py pdf_toolkit.py
```

You will see this menu:

```
--------------------------------------------------
       PDF TOOLKIT - CONSOLE APP
--------------------------------------------------
1. Merge PDFs
2. Split PDF
3. Convert PDF to Text
4. Exit
--------------------------------------------------
Enter your choice (1-4):
```

To stop the program midway, press `Ctrl + C`.

---

## How to use each option

> **Important:** When the program asks for a "path", type the **file name** (for example `a.pdf`), not a number. For testing, keep your PDF files in the same folder as `pdf_toolkit.py`. If a file is in a different folder, type its full address, for example `C:\Users\Rahul\Downloads\a.pdf`.

### Option 1: Merge PDFs

Suppose the folder contains `a.pdf` (3 pages) and `b.pdf` (2 pages).

| The program asks | You type |
|---|---|
| Enter your choice | `1` |
| How many PDF files do you want to merge? | `2` |
| Enter path for PDF #1 | `a.pdf` |
| Enter path for PDF #2 | `b.pdf` |
| Enter output file name | `merged` |

**Result:** `merged.pdf` is created with 5 pages (the 3 pages of `a.pdf` followed by the 2 pages of `b.pdf`). Files are joined in the same order in which you enter them.

If you leave out `.pdf` in the output name, the program adds it automatically.

### Option 2: Split PDF

The program counts the pages of the PDF and then offers two modes.

**Mode 1: one file per page**

| The program asks | You type |
|---|---|
| Enter your choice | `2` |
| Enter the PDF file to split | `a.pdf` |
| Enter choice (1/2) | `1` |

**Result:** A new folder named `a_split` is created containing `a_page_1.pdf`, `a_page_2.pdf` and `a_page_3.pdf`.

**Mode 2: a page range only**

| The program asks | You type |
|---|---|
| Enter choice (1/2) | `2` |
| Start page | `2` |
| End page | `3` |

**Result:** `a_pages_2-3.pdf` is created inside the `a_split` folder, containing only pages 2 and 3.

### Option 3: Convert PDF to Text

| The program asks | You type |
|---|---|
| Enter your choice | `3` |
| Enter the PDF file to convert | `a.pdf` |
| Enter output .txt file name | `mytext` (or leave blank) |

**Result:** `mytext.txt` is created. If you leave the name blank, the PDF's name is reused (`a.txt`). Inside the file, each page looks like this:

```
--- Page 1 ---
(text of page 1)

--- Page 2 ---
(text of page 2)
```

### Option 4: Exit

The program closes.

---

## Project structure

```
pdf-toolkit/
|-- pdf_toolkit.py     # The whole program (all code is in this file)
|-- README.md          # This file
```

Output files (`merged.pdf`, `.txt` files, `_split` folders) are created in the folder from which the program is run.

---

## How the code works

All the code lives in `pdf_toolkit.py` and is divided into small functions. Each function does one job.

### Imports

```python
import os
import sys
from pypdf import PdfReader, PdfWriter
import pdfplumber
```

| Import | Purpose |
|---|---|
| `os` | Working with files and folders (checking a file exists, creating folders, joining paths) |
| `sys` | Closing the program (`sys.exit`) |
| `PdfReader` | Reading a PDF file |
| `PdfWriter` | Creating a new PDF file |
| `pdfplumber` | Extracting text from a PDF |

### `clear_line()`

Prints `--------------------------------------------------` on the screen so the menu looks tidy.

### `get_valid_pdf_path(prompt)`

Asks the user for a PDF file path and **keeps asking until a valid one is entered**. It checks three things:

1. The user typed something (the input is not empty)
2. The file really exists (`os.path.isfile`)
3. The file name ends with `.pdf`

If all three checks pass, it returns the path. This function is used by merge, split and text conversion, so the checking code is written only once instead of three times.

It also cleans the input: `.strip()` removes extra spaces and `.strip('"')` removes quotes (Windows adds quotes when you use "Copy as path").

### `merge_pdfs()`

1. Asks how many files to merge (at least 2)
2. For each file, gets the path through `get_valid_pdf_path()` and stores it in a list
3. Asks for the output file name
4. Creates an empty `PdfWriter`
5. Opens each file with `PdfReader` and adds every page to the writer
6. Saves the writer to a file

If the user types letters instead of a number, the `ValueError` is caught and "Please enter a valid number" is shown.

### `split_pdf()`

1. Gets the PDF path and counts the total pages
2. Asks for the mode (1 or 2)
3. Creates an output folder named `<name>_split` (`os.makedirs`). If the folder already exists, no error occurs (`exist_ok=True`)
4. **Mode 1:** creates a new writer for each page and saves each page as its own file
5. **Mode 2:** reads the start and end page, checks that the range is valid, and saves only those pages into one file

Note: Python counts pages from 0, so the code uses `start - 1`. For the user, page 1 is still page 1.

### `pdf_to_text()`

1. Gets the PDF path
2. Gets the output `.txt` name (if blank, it uses the PDF's name)
3. Opens the PDF with `pdfplumber` and calls `extract_text()` on every page
4. Writes `--- Page N ---` above each page's text
5. Saves all the text into a `.txt` file using `utf-8` encoding (so special characters display correctly)

If a page has no text, `or ""` prevents a crash and that page is simply left empty.

### `main_menu()`

The main loop of the program. Because of `while True`, the menu keeps appearing. It reads the user's choice and calls the matching function. Choice 4 calls `sys.exit(0)` to close the program. An invalid choice shows "Invalid choice".

### Entry point

```python
if __name__ == "__main__":
    main_menu()
```

This line means: if the file is run directly (not imported from another file), start with `main_menu()`. This is where the program begins.

### Error handling

Merge, split and text conversion are all wrapped in `try / except`. If something goes wrong (for example a corrupt PDF), the program shows an `Error` message and returns to the menu instead of crashing.

---

## Program flow

```
python pdf_toolkit.py
        |
        v
   main_menu()  <---------------------------+
        |                                    |
   User choice                               |
   |      |       |        |                 |
   1      2       3        4                 |
 Merge  Split   Text     Exit (program ends) |
   |      |       |                          |
   v      v       v                          |
 merged  _split  .txt                        |
 .pdf    folder  file                        |
   |      |       |                          |
   +------+-------+---- press Enter ---------+
```

---

## Common errors and fixes

| Problem | Cause | Solution |
|---|---|---|
| `File not found: 1` | A number was typed instead of a file name | Type the real file name, such as `a.pdf` |
| `File not found: a.pdf` | The file is not in the project folder, or the name is wrong | Put the file in the same folder as `pdf_toolkit.py` and check the spelling and `.pdf` |
| `That doesn't look like a PDF file` | The file is not a `.pdf` (for example `.docx`) | Provide PDF files only |
| `python is not recognized` | Python is not on PATH, or the command name differs | Try `py pdf_toolkit.py`, or reinstall Python and tick "Add to PATH" |
| `ModuleNotFoundError: No module named 'pypdf'` | The libraries are not installed | Run `pip install pypdf pdfplumber` |
| Text file is empty | The PDF is scanned (image based) | This tool cannot read text from images (see Limitations) |
| pip shows a "dependency conflict" warning | Another package was already installed on the computer | It is only a warning and can be ignored |

---

## Limitations

- **Scanned PDFs** (made from photos) will not give any text, because there is no OCR. Only PDFs with real, selectable text work.
- **Password-protected PDFs** may produce an error.
- If an output file with the same name already exists, it is **overwritten without asking**.
- In merge, the file order is whatever the user entered. To change the order, the program has to be run again.
- Text extraction may lose the formatting of tables and complex layouts.

---

## Future improvements

- Ask for confirmation before overwriting an output file
- Merge every PDF in a folder automatically
- Split by a list of pages (for example `1,3,5-7`)
- OCR support for scanned PDFs
- An option to password-protect a PDF

---

## Authors

Name: Anmol
