# NLP-Police-Complaints

Repository with code for the CAPP30255 - Advanced Machine Learning Project

The aim of the project is to apply a Natural Language Processing Task (NLP) on the Police Complaints available at [COPA's Case Portal](https://www.chicagocopa.org/data-cases/case-portal/). There project consists of three main parts:

### 1. Scraping the data

a. With the copa_scraper.py file, located in `src/copa_scraper/copa_scraper.py`, located we scrape the data from the COPA's Case Portal and save the PDFs locally in the `data/` folder. This process also outputs some .csv files, which contain the case id, the URL of the case and the URL to its PDF.

The pipeline can be run like this, where you need the complete path to the `copa_scraper.py` script.

```python3 /NLP-Police-Complaints/src/copa_scraper/copa_scraper.py```

b. Then, we need to remove the PDF files that do not correspond to a Final Summary Report. This is done with the `remove_useles_pdfs.py` script in the `src/data_cleaning/` folder. This script reads the `copa_data_with_pdf.csv` file from the `data/` folder (this .csv file was obtained in the previous step) and removes the PDFs that do not correspond to a Final Summary Report. The script is run like this:

```python3 /NLP-Police-Complaints/src/data_cleaning/remove_useless_pdfs.py```


### 2. Extracting the text from the PDFs

This was done with Jonathan's `extractor.py` code.



