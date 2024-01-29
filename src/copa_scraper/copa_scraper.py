"""This script will extract the data from the COPA website"""

import os
import re
import time
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

# PARAMETERS
URL = "https://www.chicagocopa.org/data-cases/case-portal/"
headers = {
    "Referer": "https://www.chicagocopa.org/data-cases/case-portal/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
}

PDF_PATH = "data/"


class COPAScraper:
    PORTAL_URL = URL
    PDF_PATH = PDF_PATH

    def __init__(self):
        # Check if PDF path exists, if not, create it
        if not os.path.exists(PDF_PATH):
            os.makedirs(PDF_PATH)
            print(f"Created {PDF_PATH} directory")
        else:
            print(f"{PDF_PATH} directory already exists")

        self.headers = headers
        self.case_url = "https://www.chicagocopa.org/case"
        self.threshold = 5
        self.pdf_threshold = 10

        self.get_num_pages()
        print(f"Number of pages: {self.last_page}")

    def get_num_pages(self):
        """Gets the number of pages in the table"""
        r = requests.get(self.PORTAL_URL, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        pagination = soup.find("div", {"class": "pagination"})

        # Get text from pagination
        pagination_text = pagination.text
        pagination_text = pagination_text.replace("\n", "")

        # Use regex to extract the last page
        numbers = re.findall(r"\d+", pagination_text)
        if numbers:
            self.last_page = int(numbers[-1])
        else:
            self.last_page = 1

    @staticmethod
    def is_pdf_available(df):
        """Determines if the PDF is available or not"""

        # We need month and year of FSR Posted Date
        raw_date = str(df["FSR/Memo Posted Date"])

        if "/" in raw_date:
            return "Available"

        else:
            return "Not Available"

    def extract_table(self, url):
        """Extracts the table from the given url"""
        # Use pandas
        table_index = 0
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(StringIO(str(table)))[table_index]

        # Construct case URLs
        df.loc[:, "case_url"] = df["Log#"].apply(lambda x: f"{self.case_url}/{x}/")

        # Construct PDF URLs
        df.loc[:, "pdf_available"] = df.apply(self.is_pdf_available, axis=1)

        return df

    def extract_all_tables(self):
        """Extracts all tables from the portal"""
        dfs = []
        for num_page in range(1, self.last_page + 1):
            url = f"{self.PORTAL_URL}?sf_paged={num_page}"
            df = self.extract_table(url)
            dfs.append(df)

            if num_page % self.threshold == 0:
                print(f"Finished extracting page {num_page}")
                time.sleep(5)

        self.all_tables = pd.concat(dfs, ignore_index=True)
        return self.all_tables

    def extract_all_pdfs(self):
        """Extracts all PDFs from the portal"""
        # Get all the urls
        valid_cases = self.all_tables[self.all_tables["pdf_available"] == "Available"]
        urls = valid_cases["case_url"].values
        case_log = valid_cases["Log#"].values

        # Get all the PDF urls
        pdf_urls = []
        counter = 1
        for url, case_log in zip(urls, case_log):
            try:
                pdf_url = self.get_pdf_url(url, case_log)
            except Exception as e:
                print(f"Error: {e}")
                pdf_url = "Error"
            pdf_urls.append(pdf_url)
            if counter % self.pdf_threshold == 0:
                print(f"Finished extracting PDF {counter}")
                time.sleep(2.5)

            counter += 1

        # Add to dataframe
        valid_cases.loc[:, "pdf_url"] = pdf_urls

        return valid_cases

    def get_pdf_url(self, url, case_log):
        """
        Extract the pdf given the url
        """
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")

        # Search for element with text 'Final Summary Report'
        pdf_url = "Not Found"
        for a in soup.find_all("a", href=True):
            if "Final Summary Report" in a.text:
                pdf_url = a["href"]

        # If found, download the pdf
        if pdf_url is not None:
            r = requests.get(pdf_url, stream=True, headers=self.headers)
            with open(f"{self.PDF_PATH}/{case_log}.pdf", "wb") as f:
                f.write(r.content)

        else:
            print(f"PDF not found for {case_log}")

        return pdf_url


if __name__ == "__main__":
    scraper = COPAScraper()
    # tables = scraper.extract_all_tables()
    # tables.to_csv("copa_data.csv", index=False)
    scraper.all_tables = pd.read_csv(f"{PDF_PATH}/copa_data.csv")
    valid_cases = scraper.extract_all_pdfs()
    valid_cases.to_csv(f"{PDF_PATH}/copa_data_with_pdf.csv", index=False)
