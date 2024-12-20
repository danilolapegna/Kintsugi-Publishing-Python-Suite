#!/usr/bin/env python3

"""
Translator class for performing high-quality translations using OpenAI's API.

- Ensures tone, style, and verbosity are adapted for the target language.
- Leverages a customizable prompt for translation tasks.
- Inherits from the BaseProcessor for consistent client interaction.
"""

from .base_processor import BaseProcessor

class Translator(BaseProcessor):
    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.base_prompt = (
            "You are a translator. Translate the given text from {src} to {tgt}. "
            "Do not add comments, only return the translated text."
            "Make sure that's a high-quality translation, where things aren't just rendered literally,"
            "but the tone, verbosity and style is inferred from the original language and perfectly"
            "adapted into the destination language."
        )

def build_prompt(self):
    return self.base_prompt.format(src=self.source_lang, tgt=self.target_lang)