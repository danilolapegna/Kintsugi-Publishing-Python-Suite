#!/usr/bin/env python3

"""
GrammarReviewer class for identifying grammatical errors, typos, and inconsistencies in text using OpenAI's API.

- Provides suggestions for correcting identified issues.
- Returns 'NO SERIOUS ERRORS HERE' if no significant problems are found.
- Adjustable severity levels allow for varying strictness.
- Inherits from BaseProcessor to ensure a consistent processing framework.
"""

from .base_processor import BaseProcessor

class GrammarReviewer(BaseProcessor):

    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.base_prompt = (
            "You are a reviewer. You will receive text and return, if present, a list of grammatical "
            "errors, typos, inconsistencies, and a suggestino on how to fix each of them. If no such errors, please just"
            "return 'NO SERIOUS ERRORS HERE'."
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