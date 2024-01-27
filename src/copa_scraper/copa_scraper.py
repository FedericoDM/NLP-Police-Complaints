"""This script will extract the data from the COPA website"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


# PARAMETERS
URL = "https://www.chicagocopa.org/data-cases/case-portal/"
headers = {
    "Referer": "https://www.chicagocopa.org/data-cases/case-portal/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
}


class COPAScraper:
    PORTAL_URL = URL

    def __init__(self):
        self.headers = headers
        self.case_url = "https://www.chicagocopa.org/case"

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
    def construct_pdf_url(df):
        """Constructs the pdf url given the case number and
        the FSR Posted Date if available"""

        # Extract case number
        case_number = df["Log#"]

        # We need month and year of FSR Posted Date
        raw_date = str(df["FSR/Memo Posted Date"])

        if "/" in raw_date:
            # Extract month and year
            split_date = raw_date.split("/")
            month = split_date[0]
            year = split_date[2]

            # Construct url
            return f"https://www.chicagocopa.org/wp-content/uploads/{year}/{month}/{case_number}_FSR.pdf"

        else:
            return "Not Available"

    def extract_table(self, url):
        """Extracts the table from the given url"""
        # Use pandas
        table_index = 0
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[table_index]

        # Construct case URLs
        df.loc[:, "case_url"] = df["Log#"].apply(lambda x: f"{self.case_url}/{x}/")

        # Construct PDF URLs
        df.loc[:, "pdf_url"] = df.apply(self.construct_pdf_url, axis=1)

        return df


if __name__ == "__main__":
    scraper = COPAScraper()
    # tables = scraper.extract_table(URL)
    # tables.to_csv("copa_data.csv", index=False)
    # print(tables)
