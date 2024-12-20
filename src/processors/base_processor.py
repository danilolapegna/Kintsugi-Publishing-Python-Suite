import os
import copy
from docx import Document

class BaseProcessor:
    def __init__(self, client, severity, source_lang, target_lang):
        self.client = client
        self.severity = severity
        self.source_lang = source_lang
        self.target_lang = target_lang

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
        return "processed"

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
