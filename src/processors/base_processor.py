#!/usr/bin/env python3

"""
BaseProcessor class provides a generic framework for processing document sections.

- Includes utilities for generating updated `.docx` files by replacing text in original documents.
- Intended to be extended by specific processors like reporters or reviewers.
"""

import os
import copy
from docx import Document
from docx.enum.text import WD_BREAK

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

    def generate_docx_advanced_mode(self, original_path, sections, results, output_path):
        doc = Document(original_path)
        results_by_id = {r["id"]: r for r in results}  # Create a mapping of results by ID

        if len(sections) != len(results):
            raise ValueError("Sections and results lengths do not match.")

        # Helper function to process a paragraph
        def process_paragraph(paragraph, content, style_name):
            # Preserve non-text elements by iterating through runs
            for run in paragraph.runs:
                if run.text.strip():  # Modify text runs only
                    run.text = content if content else run.text

            # Apply styles if specified
            if style_name and style_name in [s.name for s in doc.styles]:
                paragraph.style = style_name

        # Process main document paragraphs
        for idx, paragraph in enumerate(doc.paragraphs):
            section_id = f"main-{idx}"
            rendered_info = results_by_id.get(section_id)
            if rendered_info:
                process_paragraph(paragraph, rendered_info.get("content", "").strip(), rendered_info.get("style_name", "").strip())

        # Process headers and footers
        for section in doc.sections:
            def process_section(section_type):
                paragraphs = getattr(section, section_type).paragraphs
                for idx, paragraph in enumerate(paragraphs):
                    section_id = f"{section_type}-{idx}"
                    rendered_info = results_by_id.get(section_id)
                    if rendered_info:
                        process_paragraph(paragraph, rendered_info.get("content", "").strip(), rendered_info.get("style_name", "").strip())

            process_section("header")
            process_section("footer")

        doc.save(output_path)


    def map_sections(self, sections, results):
        return {section["content"]: result for section, result in zip(sections, results)}

    def replace_text_in_sections(self, text, text_map):
        for original, translated in text_map.items():
            if original.strip() and original in text:
                text = text.replace(original, translated)
        return text

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