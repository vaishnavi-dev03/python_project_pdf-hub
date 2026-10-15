"""
PDF Toolkit - Console Based Python Project
--------------------------------------------
Features:
    1. Merge multiple PDF files into one
    2. Split a PDF into individual pages (or a page range)
    3. Convert a PDF's text content into a .txt file

Requirements:
    pip install pypdf pdfplumber
"""


import os
import sys
from pypdf import PdfReader, PdfWriter
import pdfplumber


def clear_line():
    print("-" * 50)


def get_valid_pdf_path(prompt):
    """Ask the user for a path until a valid, existing .pdf file is given."""
    while True:
        path = input(prompt).strip().strip('"')
        if not path:
            print("Please enter a file path.")
            continue
        if not os.path.isfile(path):
            print(f"File not found: {path}")
            continue
        if not path.lower().endswith(".pdf"):
            print("That doesn't look like a PDF file. Try again.")
            continue
        return path


# ---------------------------------------------------------
# 1. MERGE
# ---------------------------------------------------------
def merge_pdfs():
    clear_line()
    print("PDF MERGER")
    clear_line()
    try:
        count = int(input("How many PDF files do you want to merge? "))
        if count < 2:
            print("You need at least 2 files to merge.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    files = []
    for i in range(count):
        path = get_valid_pdf_path(f"Enter path for PDF #{i + 1}: ")
        files.append(path)

    output_path = input("Enter output file name (e.g. merged.pdf): ").strip()
    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"

    writer = PdfWriter()
    try:
        for f in files:
            reader = PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as out:
            writer.write(out)

        print(f"\n✅ Merged {count} files successfully -> {output_path}")
    except Exception as e:
        print(f"\n❌ Error while merging: {e}")


# ---------------------------------------------------------
# 2. SPLIT
# ---------------------------------------------------------
def split_pdf():
    clear_line()
    print("PDF SPLITTER")
    clear_line()
    input_path = get_valid_pdf_path("Enter the PDF file to split: ")

    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        print(f"This PDF has {total_pages} page(s).")

        print("\nChoose split mode:")
        print("1. Split into individual pages (one PDF per page)")
        print("2. Extract a specific page range into one PDF")
        mode = input("Enter choice (1/2): ").strip()

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        out_dir = f"{base_name}_split"
        os.makedirs(out_dir, exist_ok=True)

        if mode == "1":
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                out_path = os.path.join(out_dir, f"{base_name}_page_{i + 1}.pdf")
                with open(out_path, "wb") as out:
                    writer.write(out)
            print(f"\n✅ Split into {total_pages} files -> folder '{out_dir}'")

        elif mode == "2":
            start = int(input(f"Start page (1-{total_pages}): "))
            end = int(input(f"End page (1-{total_pages}): "))
            if start < 1 or end > total_pages or start > end:
                print("Invalid page range.")
                return

            writer = PdfWriter()
            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])

            out_path = os.path.join(out_dir, f"{base_name}_pages_{start}-{end}.pdf")
            with open(out_path, "wb") as out:
                writer.write(out)
            print(f"\n✅ Extracted pages {start}-{end} -> {out_path}")

        else:
            print("Invalid choice.")

    except Exception as e:
        print(f"\n❌ Error while splitting: {e}")


# ---------------------------------------------------------
# 3. PDF TO TEXT
# ---------------------------------------------------------
def pdf_to_text():
    clear_line()
    print("PDF TO TEXT CONVERTER")
    clear_line()
    input_path = get_valid_pdf_path("Enter the PDF file to convert: ")

    output_path = input(
        "Enter output .txt file name (leave blank for same name): "
    ).strip()
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".txt"
    elif not output_path.lower().endswith(".txt"):
        output_path += ".txt"

    try:
        full_text = ""
        with pdfplumber.open(input_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                full_text += f"--- Page {i + 1} ---\n{text}\n\n"
                print(f"Processed page {i + 1}/{total_pages}", end="\r")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"\n\n✅ Text extracted successfully -> {output_path}")
    except Exception as e:
        print(f"\n❌ Error while converting: {e}")


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------
def main_menu():
    while True:
        clear_line()
        print("       PDF TOOLKIT - CONSOLE APP")
        clear_line()
        print("1. Merge PDFs")
        print("2. Split PDF")
        print("3. Convert PDF to Text")
        print("4. Exit")
        clear_line()

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            merge_pdfs()
        elif choice == "2":
            split_pdf()
        elif choice == "3":
            pdf_to_text()
        elif choice == "4":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select between 1-4.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_menu()