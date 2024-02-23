"""
This script contains a class that performs all the necessary text cleaning
"""

import os

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


class TextParser:
    CHARS_TO_REMOVE = CHARS_TO_REMOVE
    REGEX_PATTERNS = REGEX_PATTERNS

    def __init__(self, path):
        self.path = path

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
