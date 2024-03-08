"""
This class works as a wrapper for the Hugging Face API for the summarizer model
"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class Summarizer:
    """
    This class is in charge of summarizing a given text using
    any Hugging Face model
    """

    BART_INPUT_SIZE = 1024

    def __init__(self, model_name: str, complaint_text: str, input_size: int = 2048):
        self.model_name = model_name
        self.complaint_text = complaint_text
        self.input_size = input_size

        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if self.model_name == "facebook/bart-large-cnn":
            self.inputs = self.tokenizer(
                self.complaint_text,
                return_tensors="pt",
                max_length=self.BART_INPUT_SIZE,
                truncation=True,
            )

        else:
            self.inputs = self.tokenizer(
                self.complaint_text,
                return_tensors="pt",
                max_length=self.input_size,
                truncation=True,
            )

    def generate_summary(
        self,
        max_length: int = 1200,
        min_length: int = 40,
        length_penalty: float = 2.0,
        no_repeat_ngram_size: int = 2,
        num_beams: int = 4,
        early_stopping: bool = True,
    ):
        """
        This function will generate the summary with the given parameters
        """

        # Generate summary
        summary_ids = self.model.generate(
            self.inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=length_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            num_beams=num_beams,
            early_stopping=early_stopping,
        )

        # Decode and print the summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary
