#!/usr/bin/env python3

"""
GrammarReviewer class for identifying grammatical errors, typos, and inconsistencies in text using OpenAI's API.

- Provides suggestions for correcting identified issues.
- Returns 'NO SERIOUS ERRORS HERE' if no significant problems are found.
- Adjustable severity levels allow for varying strictness.
- Inherits from BaseProcessor to ensure a consistent processing framework.
"""

from .base_openai_processor import BaseOpenAIProcessor

class GrammarReviewer(BaseOpenAIProcessor):

    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.severity = min(max(processor_parameters.get('severity', 3), 1), 5)

        self.base_prompt = (
            "You are a reviewer. You will receive text. If any grammatical errors, typos, or inconsistencies "
            "are present, list them and provide suggestions on how to fix each of them. "
            "Your response should be in the same language as the input text. "
            "If you find no errors, return: NO SERIOUS ERRORS HERE."
    )
        
    def output_suffix(self):
        return "reviewed"

    def build_prompt(self):
        sev_map = {
            1: "very lenient",
            2: "lenient",
            3: "normal",
            4: "strict",
            5: "very strict"
        }
        return f"{self.base_prompt}\nDo it with a severity level that's {sev_map.get(self.severity, 'normal')}"

    def postprocess(self, response, section):
        if response.lower() == "no serious errors here":
            return None
        return response