#!/usr/bin/env python3

"""
Parses documents into structured sections based on headings and content.

- Supports `.docx` and plain text files.
- Merges sections with low word count below a configurable threshold.
- Customizable heading styles determine section boundaries.
"""

import os
from docx import Document

class DocumentParser:
    def __init__(self, heading_styles, min_word_threshold=2):
        self.heading_styles = heading_styles
        self.min_word_threshold = min_word_threshold

    def parse_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".docx":
            return self._parse_docx(file_path)
        else:
            return self._parse_text(file_path)

    def _parse_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        if not text:
            return []
        return [{"title": "Document", "content": text}]

    def _parse_docx(self, file_path):
        document = Document(file_path)
        paragraphs = document.paragraphs
        sections = []
        current_section = []
        for paragraph in paragraphs:
            style_name = paragraph.style.name if paragraph.style else ""
            if style_name in self.heading_styles:
                if current_section:
                    sections.append(current_section)
                current_section = [paragraph.text]
            else:
                if current_section:
                    current_section.append(paragraph.text)
        if current_section:
            sections.append(current_section)
        merged_sections = []
        i = 0
        while i < len(sections):
            section = sections[i]
            title = section[0] if section else "Untitled"
            content = "\n".join(section[1:]).strip()
            word_count = len(content.split())
            j = i
            while word_count < self.min_word_threshold and j + 1 < len(sections):
                j += 1
                next_sec = sections[j]
                content += "\n".join(next_sec)
                word_count = len(content.split())
            merged_sections.append({"title": title, "content": content})
            i = j + 1
        return merged_sections
