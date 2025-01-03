#!/usr/bin/env python3

"""
BaseOpenAIProcessor class provides an OpenAI-dependent framework for processing document sections.

- Specific BaseProcessor, designed to handle OpenAI client interactions with custom prompts.
- Intended to be extended by specific processors like translators or reviewers.
"""

from .base_processor import BaseProcessor

class BaseOpenAIProcessor(BaseProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        self.additional_prompt = processor_parameters.get('additional_prompt', '')
        
    def process_sections(self, sections):
        results = []
        idx = 0
        for s in sections:
            section_id = s.get("id", idx)

            # Skip API calls and return as-is for content defined by this method (default: empty or all-whitespaces)
            if self.do_not_process(s):
                results.append({"id": section_id, "content": s["content"]})  # Preserve ID for empty sections
                continue

            # Else call the API only for content that passes the check
            c = self.client.get_completion(f"{self.build_prompt()}. {self.additional_prompt}", s["content"])
            if c:
                # Wrap the result in a dictionary with the necessary keys
                res = {"id": section_id, "content": c}
                results.append(res)
        idx+=1
        return results

    # Sections matching this criteria will not be sent to OpenAI and just added as-they-are to mapping
    def do_not_process(self, section):
        return not section["content"].strip()

    def build_prompt(self):
        return ''

    def output_suffix(self):
        return "ai_processed"