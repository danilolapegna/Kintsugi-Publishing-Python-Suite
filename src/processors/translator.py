#!/usr/bin/env python3

"""
Translator class for performing high-quality translations using OpenAI's API.

- Ensures tone, style, and verbosity are adapted for the target language.
- Leverages a customizable prompt for translation tasks.
- Inherits from the BaseProcessor for consistent client interaction.
"""

from .base_openai_processor import BaseOpenAIProcessor

class Translator(BaseOpenAIProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.source_lang = processor_parameters['source_lang']
        self.target_lang = processor_parameters['target_lang']
        
        self.base_prompt = (
            "You are a translator. Translate the given text from {src} to {tgt}. "
            "Do not add comments, only return the translated text. "
            "If text is empty do not comment that. Simply return with an empty string yourself."
            "If text cannot be translated as it's a name, number or symbols do not comment that. Simply return with the original text."
            "Make sure that's a high-quality translation, where things aren't just rendered literally, "
            "but the tone, verbosity and style is inferred from the original language and perfectly "
            "adapted into the destination language. "
        )

    def output_suffix(self):
        return f"translated_{self.source_lang}_{self.target_lang}"

    def build_prompt(self):
        return self.base_prompt.format(src=self.source_lang, tgt=self.target_lang)