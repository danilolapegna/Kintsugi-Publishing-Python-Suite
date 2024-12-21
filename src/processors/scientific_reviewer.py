#!/usr/bin/env python3

"""
ScientificReviewer class for identifying factual and scientific errors in text using OpenAI's API.

- Compares text against the highest-level academic research for accuracy.
- Allows adjustable severity levels for leniency or strictness in reviews.
- Returns 'NO FACTUAL ERRORS HERE' if no issues are found.
- Inherits from BaseProcessor to maintain consistency across processors.
"""

from .base_openai_processor import BaseOpenAIProcessor

class ScientificReviewer(BaseOpenAIProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.severity = min(max(processor_parameters['severity'], 1), 5)

        self.base_prompt = (
            "You are a scientific reviewer. You will receive text and return all the possible factual "
            "and scientific errors, and what's correc there. Make sure that's compared against the highest "
            "level and more reliable academic research on the subject. "
            "The output needs to be in the same language as the input text. "
            "If instead there are none, return 'NO FACTUAL ERRORS HERE'. "
        )
        
    def output_suffix(self):
        return "scientifically_reviewed"
    
    def build_prompt(self):
        sev_map = {
            1: "very lenient",
            2: "lenient",
            3: "normal",
            4: "strict",
            5: "very strict"
        }
        return f"{self.base_prompt}\nDo this scientific check with a severity level that's {sev_map.get(self.severity, 'normal')}"

    def postprocess(self, response, section):
        if response.lower() == "no factual errors here":
            return None
        return response