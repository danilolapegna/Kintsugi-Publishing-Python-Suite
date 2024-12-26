#!/usr/bin/env python3

"""
BaseProcessor class provides a generic framework for processing document sections.

- Includes utilities for generating updated `.docx` files by replacing text in original documents.
- Intended to be extended by specific processors like reporters or reviewers.
"""

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