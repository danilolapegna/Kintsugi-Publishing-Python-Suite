#!/usr/bin/env python3

"""
ScientificReviewer class for identifying factual and scientific errors in text using OpenAI's API.

- Compares text against the highest-level academic research for accuracy.
- Allows adjustable severity levels for leniency or strictness in reviews.
- Returns 'NO FACTUAL ERRORS HERE' if no issues are found.
- Inherits from BaseProcessor to maintain consistency across processors.

Needs to be augmented via additional, professional research and checks on sites
like scite.ai or Pubmed.

"""

from .base_openai_processor import BaseOpenAIProcessor

class ScientificReviewer(BaseOpenAIProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.severity = min(max(processor_parameters.get('severity', 3), 1), 5)

        self.base_prompt = (
            "You are a scientific reviewer. You will receive a piece of text. Your task is to:"
            " 1) Identify any factual or scientific errors, referencing the most reliable academic research."
            " 2) Provide the correct information or clarification for each error."
            " 3) Deliver your analysis in the same language as the input text."
            " If there are no factual or scientific inaccuracies, respond with: NO FACTUAL ERRORS HERE."
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
    
    # Let's skip processing for all sections with less than 2 words, as it probably doesn't make sense to science-review them
    def do_not_process(self, section):
        return not section["content"].strip() or len(section["content"].split()) < 2

    def postprocess(self, response, section):
        if response.lower() == "no factual errors here":
            return None
        return response