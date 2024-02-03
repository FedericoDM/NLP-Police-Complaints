"""This script removes PDFs that are not useful for the project"""

import os
import pandas as pd

# PARAMETERS

# Path to the PDFs

PDF_PATH = "data/"


# Read dataframe with the data
class PDFCleaner:
    PDF_PATH = PDF_PATH
    STRING_TO_CHECK = "how-to-read-a-case-summary-report"

    def __init__(self):
        self.copa_df = pd.read_csv("data/copa_data_with_pdf.csv")

    def get_useless_pdfs(self):
        """Get the PDFs that are not useful"""
        # Get the PDFs that are not useful
        self.useless_pdfs = self.copa_df.loc[
            self.copa_df["pdf_url"].str.contains(self.STRING_TO_CHECK), :
        ].copy()

        self.useless_pdfs.reset_index(drop=True, inplace=True)

        self.useless_pdfs.to_csv("data/useless_pdfs.csv", index=False)

        return self.useless_pdfs

    def remove_useless_pdfs(self):
        """Remove the PDFs that are not useful"""
        # Get the PDFs that are not useful
        if not hasattr(self, "useless_pdfs"):
            self.get_useless_pdfs()

        # Remove the PDFs that are not useful
        for pdf in self.useless_pdfs["Log#"]:
            try:
                os.remove(f"{self.PDF_PATH}/{pdf}.pdf")
                print(f"File {pdf}.pdf removed")
            except FileNotFoundError:
                print(f"File {pdf}.pdf not found")

        print("Useless PDFs removed")


# Main
if __name__ == "__main__":
    cleaner = PDFCleaner()
    useless_pdfs = cleaner.get_useless_pdfs()
    cleaner.remove_useless_pdfs()
