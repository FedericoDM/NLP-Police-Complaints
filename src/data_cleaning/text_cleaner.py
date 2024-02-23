"""
This script contains a class that performs all the necessary text cleaning 
for the current NLP tasks
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


# CONSTANTS

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


# consider customizing the list of stopwords more to remove very common words
CUSTOM_STOPS = [
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
FINDING_STOPS = ["sustained", "not sustained", "unfounded", "exonerated"]


class TextParser:
    CHARS_TO_REMOVE = CHARS_TO_REMOVE
    REGEX_PATTERNS = REGEX_PATTERNS
    HEADERS = HEADERS
    CUSTOM_STOPS = CUSTOM_STOPS
    FINDING_STOPS = FINDING_STOPS

    def __init__(
        self,
        path,
        nlp_task,
        add_more_stops=False,
        findings_are_stops=False,
    ):
        self.path = path

        if nlp_task == "topic modeling":

            print("Initializing parsers for topic modeling...")
            self.stemmer = SnowballStemmer(language="english")
            self.lemmatizer = WordNetLemmatizer()
            self.stops = list(stopwords.words("english"))

            if add_more_stops:
                self.stops += self.CUSTOM_STOPS

            if findings_are_stops:
                self.stops += self.FINDING_STOPS

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

    def file_to_string(self, filename, lower_text=True):
        """
        Add each line of a text file to a string, text is
        lowercased by default
        """
        text = ""
        file_path = os.path.join(self.path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                for char in self.CHARS_TO_REMOVE:
                    line = line.replace(char, "")
                text += line

        text = text.strip()
        if lower_text:
            text = text.lower()
        text = re.sub(r"\s+", " ", text)

        # Remove REGEX patterns
        for pattern in self.REGEX_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text

    def preprocess(
        self,
        data: str,
        remove_stops=True,
        stem=True,
        lemmatize=True,
        return_as_list=True,
    ):
        """Pre-process the contents of a .txt file."""
        data = re.sub("\n", " ", data)
        data = data.lower()
        data = re.sub(r"[^\w\s]|/|\_", "", data)
        data = re.sub(r"\d+", "", data)  # remove all numbers
        data = re.sub(HEADERS, "", data)

        data = data.split(" ")
        if remove_stops:
            data = [w for w in data if w not in self.stops]
            if stem:
                data = [self.stemmer.stem(w) for w in data]
            elif lemmatize:  # TODO: try both and see what happens
                data = [self.lemmatizer.lemmatize(w) for w in data]
        if return_as_list:
            return [w for w in data if w != ""]
        else:
            return " ".join(data)

    def get_full_corpus(
        self,
        preprocess_input=True,
        stem_input=False,
        lemmatize_input=False,
        print_progress=False,
    ):
        """
        Extract text from every .txt file in a folder.
        Returns (list): a corpus, with each document's text as a single
        long string
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
                    data = self.preprocess(
                        data,
                        stem=stem_input,
                        lemmatize=lemmatize_input,
                        return_as_list=False,
                    )
                corpus.append(data)

        if print_progress:
            print("Corpus text extraction complete")
        return corpus
