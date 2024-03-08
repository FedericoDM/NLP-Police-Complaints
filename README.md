# NLP-Police-Complaints

Repository with code for the CAPP30255 - Advanced Machine Learning Project

Team members:

- Jonathan Juarez
- Matt Jackson
- Federico Dominguez Molina

The aim of the project is to apply a Natural Language Processing Task (NLP) to gain insights on the Police Complaints available at [COPA's Case Portal](https://www.chicagocopa.org/data-cases/case-portal/). There project consists of three main parts:

### 1. Scraping the data

a. With the copa_scraper.py file, located in `src/copa_scraper/copa_scraper.py`, located we scrape the data from the COPA's Case Portal and save the PDFs locally in the `data/` folder. This process also outputs some .csv files, which contain the case id, the URL of the case and the URL to its PDF.

The pipeline can be run like this, where you need the complete path to the `copa_scraper.py` script.

```bash 
python3 /NLP-Police-Complaints/src/copa_scraper/copa_scraper.py
```

b. Then, we need to remove the PDF files that do not correspond to a Final Summary Report. This is done with the `remove_useles_pdfs.py` script in the `src/data_cleaning/` folder. This script reads the `copa_data_with_pdf.csv` file from the `data/` folder (this .csv file was obtained in the previous step) and removes the PDFs that do not correspond to a Final Summary Report. The script is run like this:

```bash
python3 /NLP-Police-Complaints/src/data_cleaning remove_useless_pdfs.py
```


### 2. Extracting the text from the PDFs

This was done using `extractor.py`. PyPDF2 library was used to extract the text from each PDF file iteratively, then compiled into CSV format to analyze for correct extraction. After this step, text blocks from each log report were placed into respective txt files.

Note that this script roughly takes 2 hours to run. Greater efficiency can be done by tweaking parts of the code or using a different PDF extractor package.


## 3. Natural Language Processing (NLP) tasks

This is the main part of the project since it involves the application of NLP techniques to the extracted reports.

One can find the NLP pipelines and analysis in the `exploratory/` folder. Within the folder, each team member created their own notebook with an initial exploratory analysis. Also, each team member created different notebooks and files as required for their specific NLP task.

Note that each team member pursued a different NLP task. Jonathan focused on Named Entity Recognition (NER), Matt focused on topic modeling, and Federico focused on summarization. Moreover, the unified text cleaning procedure (`text_parser.py`) along with the name stops file (`name_stops.py`) are also located in this folder.


## Additional Information

**Data Cleaning**

In order to create a unified cleaning procedure, we created the `TextParser` class in the `text_parser.py` file (which was mentioned in the previous section). This class contains methods to clean the text, such as removing punctuation, removing stop words, lemmatizing, etc. Note that several constants are defined _within_ the file.

Moreover, there is an additional pipeline used to remove PDFs that do not correspond to a Final Summary Report. This is done with the `remove_useles_pdfs.py` script in the `src/data_cleaning/` folder. This script reads the `copa_data_with_pdf.csv` file from the `data/` folder (this .csv file was obtained in the previous step) and removes the PDFs that do not correspond to a Final Summary Report. 


The class works as follows:

```python
from text_parser import TextParser

# Add the path to the text files
PATH = "path/to/text_files"

# Create the TextCleaner object, be sure to specify the NLP task
text_parser = TextParser(PATH, nlp_task="summarization")

# Random complaint file to string 
complaints = os.listdir(PATH)
complaints = [complaint for complaint in 
             complaints if complaint.endswith(".txt")]
complaints = random.sample(complaints, 1)


# The text can be used for later NLP tasks

complaint_text = text_parser.file_to_string(complaint)

```

If one were to do topic modeling, this would work as follows:

```python
from text_parser import TextParser

# Add the path to the text files
PATH = "path/to/text_files"

text_parser = TextParser(PATH, nlp_task="topic_modeling")

raw_corpus = text_parser.get_full_corpus()
print("Raw corpus complete")
stemmed_corpus = text_parser.get_full_corpus(stem_input=True)
print("Stemmed corpus complete")
lemmatized_corups = text_parser.get_full_corpus(lemmatize_input=True)
print("Lemmatized corpus complete")
```
