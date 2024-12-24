#!/usr/bin/env python3

"""
Parses documents into structured sections based on headings and content.

- Supports `.docx`, plain text files, and `.pdf`.
- Merges sections with low word count below a configurable threshold (for DOCX).
- Customizable heading styles determine section boundaries (for DOCX).
- PDF documents are split by page, each becoming its own section.
- Can return sections with or without title, depending on the param in main
"""

import os
from docx import Document
from PyPDF2 import PdfReader

class DocumentParser:
    def __init__(self, heading_styles, min_word_threshold=2, add_section_title=True):
        """
        :param heading_styles: A set or list of style names considered headings in DOCX.
        :param min_word_threshold: Sections below this word count will be merged with the next.
        """
        self.heading_styles = heading_styles
        self.min_word_threshold = min_word_threshold
        self.add_section_title = add_section_title

    def parse_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".docx":
            return self._parse_docx(file_path)
        elif ext == ".pdf":
            return self._parse_pdf(file_path)
        else:
            return self._parse_text(file_path)

    def _parse_text(self, file_path):
        """
        Parses a plain text file as a single section.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        if not text:
            return []
        if self.add_section_title:
            return [{"title": "Document", "content": text}]
        else:
            return [{"content": text}]

    def _parse_docx(self, file_path):
        """
        Parses a DOCX file by headings, merging smaller sections below a threshold.
        """
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
                content += "\n" + "\n".join(next_sec)
                word_count = len(content.split())

            if self.add_section_title:
                merged_sections.append({"title": title, "content": content})
            else:
                merged_sections.append({"content": content})
            i = j + 1
        return merged_sections

    def _parse_pdf(self, file_path):
        """
        Parses a PDF file by splitting each page into its own section.
        """
        reader = PdfReader(file_path)
        sections = []

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            # Use "Page X" as title for each PDF page.
            if self.add_section_title:
                sections.append({"title": f"PDF Page {i + 1}", "content": page_text or ""})
            else:
                sections.append({"content": page_text or ""})
        return sections
