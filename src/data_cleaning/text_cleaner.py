"""
This script contains a class that performs all the necessary text cleaning
"""

import os
import re

import nltk

nltk.download(
    "stopwords"
)  # https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import (
    SnowballStemmer,
)  # https://www.geeksforgeeks.org/snowball-stemmer-nlp/

CHARS_TO_REMOVE = ["\n", "§"]
REGEX_PATTERNS = [
    r"civilian office of police accountability\s+",
    r"log\s*\#\s*\d+",
    r"-\s*\d+\s*\d+",
    r"summary report of investigation\s+",
    r"i.\s+executive\s+summary",
    r"_+",
    r"\s*date of incident:\s*\w+\s+\d+,\s+\d+",
    r"\s*time of incident:\s*\d+:\d+\w+",
    r"\s*location of incident:\s*\d+\w+\s*\w+",
    r"\s*date of copa notification:\s*\w+\s+\d+,\s+\d+",
    r"\s*time of copa notification:\s*\d+:\d+\w+",
    r"applicable rules and laws|"
    r"conclusion|"
    r"digital evidence|"
    r"documentary evidence|"
    r"legal standard|",
    r"appendix\s+.*",
    r"\s+deputy chief administrator\s+",
    r"\s+deputy chief investigator\s+",
    r"\s+ibid\s+",
]


add_more_stops = False
findings_are_stops = False
if add_more_stops:
    # consider customizing the list of stopwords more to remove very common words
    custom_stops = [
        "officer",
        "chicago",
        "il",
        "illinois",
        "copa",
        "th",
        "",
        "incident",
        "ms",
        "mrs",
        "mr",
        "ipra",
    ]
    stops += custom_stops
if findings_are_stops:
    finding_stops = ["sustained", "not sustained", "unfounded", "exonerated"]
    stops += finding_stops

HEADERS = re.compile(
    r"independent police review authority|"
    r"civilian office of police accountability|"
    r"log#?\d+|"
    r"summary report of investigation|"
    r"executive summary|"
    r"involved parties|"
    r"allegations|"
    r"alleged that|"
    r"applicable rules and laws|"
    r"conclusion|"
    r"digital evidence|"
    r"documentary evidence|"
    r"legal standard|"
    r"preponderance of (the |)evidence|"
    r"more likely than not|"
    r"clear and convincing( evidence|)|"
    r"recommended (discipline|penalty)"
    r"violation noted"
    r"xxx*|bbb+|"  # i think this is how some redactions get turned into .txt
    r"\_+",
    re.IGNORECASE,
)


class TextParser:
    CHARS_TO_REMOVE = CHARS_TO_REMOVE
    REGEX_PATTERNS = REGEX_PATTERNS
    HEADERS = HEADERS

    def __init__(self, path, nlp_task):
        self.path = path

        if nlp_task == "topic modeling":
            self.stemmer = SnowballStemmer(language="english")
            self.lemmatizer = WordNetLemmatizer()
            self.stops = list(stopwords.words("english"))

    def txt_to_list(self, filename):
        """
        Add each line of a text file to a list
        """

        file_path = os.path.join(self.path, filename)
        lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().split()
                lines.append(line)

        return lines

    def file_to_string(self, filename):
        """
        Add each line of a text file to a string
        """
        text = ""
        file_path = os.path.join(self.path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                for char in self.CHARS_TO_REMOVE:
                    line = line.replace(char, "")
                text += line

        text = text.strip()
        text = text.lower()
        text = re.sub(r"\s+", " ", text)

        # Remove REGEX patterns
        for pattern in self.REGEX_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text

    def preprocess(
        data: str, remove_stops=True, stem=True, lemmatize=True, return_as_list=True
    ):
        """Pre-process the contents of a .txt file."""
        data = re.sub("\n", " ", data)
        data = data.lower()
        data = re.sub(r"[^\w\s]|/|\_", "", data)
        data = re.sub(r"\d+", "", data)  # remove all numbers
        data = re.sub(HEADERS, "", data)

        data = data.split(" ")
        if remove_stops:
            data = [w for w in data if w not in stops]
            if stem:
                data = [stemmer.stem(w) for w in data]
            elif lemmatize:  # TODO: try both and see what happens
                data = [lemmatizer.lemmatize(w) for w in data]
        if return_as_list:
            return [w for w in data if w != ""]
        else:
            return " ".join(data)

    def get_full_corpus(
        preprocess_input=True,
        stem_input=False,
        lemmatize_input=False,
        print_progress=False,
    ):
        """
        Extract text from every .txt file in a folder.
        Returns (list): a corpus, with each document's text as a single long string
        """
        DIR = os.path.join(os.getcwd(), "text_files")
        print(DIR)

        corpus = []

        for i, filename in enumerate(os.listdir(DIR)):
            if print_progress and i % 100 == 0:
                print(f"Extracting text from file {i}...")
            if filename.endswith(".txt"):
                filepath = os.path.join(DIR, filename)
                with open(filepath, "r") as f:
                    data = "".join(f.readlines())
                data = re.sub("\n", " ", data)
                if preprocess_input:
                    data = preprocess(
                        data,
                        stem=stem_input,
                        lemmatize=lemmatize_input,
                        return_as_list=False,
                    )
                corpus.append(data)

        if print_progress:
            print("Corpus text extraction complete")
        return corpus

    # Hyperparameter to tune: whether corpus is stemmed, lemmatized, both, or neither
    raw_corpus = get_full_corpus()
    print("Raw corpus complete")
    stemmed_corpus = get_full_corpus(stem_input=True)
    print("Stemmed corpus complete")
    lemmatized_corups = get_full_corpus(lemmatize_input=True)
    print("Lemmatized corpus complete")
