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

        for section in sections:
            rendered_info = results_by_id.get(section["id"])
            if not rendered_info or not isinstance(rendered_info, dict):
                continue

            content = rendered_info.get('content', '').strip()
            style_name = rendered_info.get('style_name', '').strip()

            # Find the matching paragraph in the document using the section ID
            for idx, paragraph in enumerate(doc.paragraphs):
                if idx == section["id"]:
                    # Save original styles and formatting
                    original_style = paragraph.style
                    original_runs = paragraph.runs  # Save all runs to preserve formatting
                    original_font_name = original_runs[0].font.name if original_runs else None
                    original_font_size = original_runs[0].font.size if original_runs else None
                    has_page_break = any(run._element.xpath('.//w:br[@w:type="page"]') for run in original_runs)

                    # Replace the text content only
                    if content:
                        for run in original_runs:
                            run.text = ''  
                        new_run = paragraph.add_run(content)
                        paragraph.style = style_name if style_name in [s.name for s in doc.styles] else original_style

                        # Restore original font settings
                        if original_font_name:
                            new_run.font.name = original_font_name
                        if original_font_size:
                            new_run.font.size = original_font_size
                    else:
                        for run in original_runs:
                            run.text = ''

                    # Reapply page break if needed
                    if has_page_break:
                        run = paragraph.add_run()
                        run.add_break(WD_BREAK.PAGE)

                    break

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