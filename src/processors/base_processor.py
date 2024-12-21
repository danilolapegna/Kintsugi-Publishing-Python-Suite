#!/usr/bin/env python3

"""
BaseProcessor class provides a generic framework for processing document sections.

- Includes utilities for generating updated `.docx` files by replacing text in original documents.
- Intended to be extended by specific processors like reporters or reviewers.
"""

import os
import copy
from docx import Document

class BaseProcessor:
    def __init__(self, client, processor_parameters):
        self.client = client
        self.processor_parameters = processor_parameters

    # Override this to declare sections processing logic
    def process_sections(self, sections):
        return sections

    # Override this to declare section postprocessing logic
    def postprocess(self, response, section):
        return response

    def output_suffix(self):
        return "processed"

    # File utility to output a docx
    def generate_docx(self, original_path, sections, results, output_path):
        doc = Document(original_path)
        text_map = self.map_sections(sections, results)
        for p in doc.paragraphs:
            original_text = p.text
            replaced = self.replace_text_in_sections(original_text, text_map)
            p.text = replaced
        doc.save(output_path)

    def map_sections(self, sections, results):
        mapping = {}
        idx = 0
        for s in sections:
            mapping[s["content"]] = results[idx] if idx < len(results) else s["content"]
            idx += 1
        return mapping

    def replace_text_in_sections(self, text, text_map):
        for k, v in text_map.items():
            if k.strip() and k in text:
                text = text.replace(k, v)
        return text