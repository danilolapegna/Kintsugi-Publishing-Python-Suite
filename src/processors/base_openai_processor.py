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
        self.additional_prompt = processor_parameters.get('additional_prompt', '')
        
    def process_sections(self, sections):
        results = []
        for s in sections:
            # Skip API call for empty or whitespace-only content
            if not s["content"].strip():
                results.append({"id": s["id"], "content": s["content"]})  # Preserve ID for empty sections
                continue

            # Call the API only for non-empty content
            c = self.client.get_completion(f"{self.build_prompt()}. {self.additional_prompt}", s["content"])
            if c:
                # Wrap the result in a dictionary with the necessary keys
                res = {"id": s["id"], "content": c}
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