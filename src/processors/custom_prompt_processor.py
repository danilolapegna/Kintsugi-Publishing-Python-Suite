#!/usr/bin/env python3

"""
CustomPromptProcessor class for allowing a completely custom prompt to be sent to OpenAI's API.

- Will simply process the document via the prompts defined via CLI as prompt and --additional-prompt
"""

from .base_openai_processor import BaseOpenAIProcessor

class CustomPromptProcessor(BaseOpenAIProcessor):

    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.base_prompt = processor_parameters.get('prompt', '')
        
    def output_suffix(self):
        return "processed"

    def build_prompt(self):
        return f"{self.base_prompt}\n{self.additional_prompt, ''}"