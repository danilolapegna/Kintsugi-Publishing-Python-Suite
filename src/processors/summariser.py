#!/usr/bin/env python3

"""
Summariser

A class that extends `BaseOpenAIProcessor` to provide functionality for summarising 
text using an OpenAI client. This processor is tailored for generating concise 
summaries while maintaining accuracy and clarity, with support for multilingual input.
"""

from .base_openai_processor import BaseOpenAIProcessor

class Summariser(BaseOpenAIProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        
        self.base_prompt = (
            "You are an expert copywriter expert in summarisation. You will receive a piece of text. Your task is to: "
            "1) Generate a summarised version that captures all the most relevant point of the text. "
            "2) Ensure the summary is accurate, clear, and written in the same language as the input text. "
            "If text cannot be translated as it's a name, number or symbols do not comment that. Simply return with the original text. "
        )

    def output_suffix(self):
        return "summarised"

    def build_prompt(self):
        return self.base_prompt
    
    # Let's skip processing for all sections with less than 6 words, as it probably doesn't make sense to summarise them
    def do_not_process(self, section):
        return not section["content"].strip() or len(section["content"].split()) < 6