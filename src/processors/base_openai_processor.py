#!/usr/bin/env python3

"""
BaseOpenAIProcessor class provides an OpenAI-dependent framework for processing document sections.

- Specific BaseProcessor, designed to handle OpenAI client interactions with custom prompts.
- Supports postprocessing of API responses and mapping results back to original content.
- Intended to be extended by specific processors like translators or reviewers.
"""

import os
import copy
from docx import Document
from .base_processor import BaseProcessor

class BaseOpenAIProcessor(BaseProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)

    def process_sections(self, sections):
        results = []
        for s in sections:
            c = self.client.get_completion(self.build_prompt(), s["content"])
            if c:
                res = self.postprocess(c, s)
                if res:
                    results.append(res)
        return results

    def build_prompt(self):
        return ''

    def postprocess(self, response, section):
        return response

    def output_suffix(self):
        return "ai_processed"

    def replace_text_in_sections(self, text, text_map):
        for k, v in text_map.items():
            if k.strip() and k in text:
                text = text.replace(k, v)
        return text