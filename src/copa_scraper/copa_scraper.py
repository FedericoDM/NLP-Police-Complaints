"""This script will extract the data from the COPA website"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the COPA website
URL = "https://www.chicagocopa.org/data-cases/case-portal/"


class COPAScraper:
    def __init__(self):
        pass
