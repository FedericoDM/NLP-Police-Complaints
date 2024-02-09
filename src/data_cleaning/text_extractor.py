"""This script extracts the files from all PDFs"""

import csv
import os
import re

import pandas as pd
import PyPDF2
from src.constants import repo_root

# set path to local directory
path = repo_root / "data/pdfs"
pdf_files = [file for file in os.listdir(path) if file.endswith(".pdf")]

if pdf_files:
    print(f"Total PDF files found in the specified path: {len(pdf_files)}")
else:
    print("No PDF files found in the specified path.")


def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        # Extract text from each page
        text_data = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text_data += page.extract_text()

        # Clean up the text to remove special characters (if needed)
        # text_data = re.sub(r'[^\w\s]', '', text_data)

        return text_data


def process_all_pdfs(directory_path, output_csv_path):
    pdf_files = [file for file in os.listdir(directory_path) if file.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Log#", "Text"])

        total_pdfs_processed = 0

        for pdf_file in pdf_files:
            log_number = pdf_file.replace(".pdf", "")
            pdf_file_path = os.path.join(directory_path, pdf_file)
            text_data = extract_text_from_pdf(pdf_file_path)
            csv_writer.writerow([log_number, text_data])

            total_pdfs_processed += 1

            # print progress after processing each PDF
            print(log_number)
            print(f"PDFs processed: {total_pdfs_processed}")


# This attempts to extract text from all pds, then stores it into text_data.csv
directory_path = "/data/pdfs"
output_csv_path = directory_path / "text_data.csv"

process_all_pdfs(path, output_csv_path)

# try using other extractor libraries as the above didn't work to extract all text
# text from 30 reports missing

# pip install pdfplumber PyMuPDF PyPDFium

# import fitz  # PyMuPDF

# def extract_text_from_pdf(pdf_file_path):
#     try:
#         with open(pdf_file_path, 'rb') as file:
#             # Use PyMuPDF (MuPDF)
#             reader = fitz.open(file)
#             num_pages = reader.page_count
#             text_data = ""

#             for page_num in range(num_pages):
#                 page = reader.load_page(page_num)
#                 text_data += page.get_text()

#             # Clean up the text if needed
#             # text_data = re.sub(r'[^\w\s]', '', text_data)

#             return text_data
#     except Exception as e:
#         print(f"Error extracting text from {pdf_file_path}: {e}")
#         return ""


# create txt files for each extracted log report
df = pd.read_csv(output_csv_path)
output_folder = path / "text_files"
os.makedirs(output_folder, exist_ok=True)

for index, row in df.iterrows():
    log_number = str(row["Log#"])
    text_data = str(row["Text"])

    filename = os.path.join(output_folder, f"{log_number}.txt")

    # Save the text as a .txt file
    with open(filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(text_data)
