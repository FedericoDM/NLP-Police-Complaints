"""This script will extract the data from the COPA website"""

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

    def extract_table(self, url):
        """Extracts the table from the given url"""
        # Use pandas
        table_index = 0
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[table_index]

        # Construct case URLs
        df.loc[:, "case_url"] = df["Case Number"].apply(
            lambda x: f"{self.case_url}/{x}/"
        )

        return df


if __name__ == "__main__":
    scraper = COPAScraper()
    tables = scraper.extract_table(URL)
    print(tables)
