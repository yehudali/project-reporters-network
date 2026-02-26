from logging import Logger
import re

class TextCleaner:
    def __init__(self, logger:Logger) -> None:
        self.logger = logger

    def clean_text(self, text:str):

        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return cleaned
