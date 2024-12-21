#!/usr/bin/env python3

"""
This script processes documents by applying tasks like grammar reviews, translations, or reports 
using modular processors and OpenAI's API. It scans documents from an input directory, processes 
sections based on a YAML configuration or CLI arguments, and generates output in text or Word format. 
Supports customization for heading styles, languages, and output formats.
"""

import argparse
import logging
import os
from config_manager import ConfigManager
from file_utils import find_documents, ensure_directory
from document_parser import DocumentParser
from openai_client import OpenAIClient
from processors import base_processor

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--input-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--heading-styles", nargs="+")
    parser.add_argument("--prompt")
    parser.add_argument("--processor")
    parser.add_argument("--severity", type=int)
    parser.add_argument("--source-lang")
    parser.add_argument("--target-lang")
    parser.add_argument("--output-format", choices=["txt","docx"])
    args = parser.parse_args()
    return args

def load_processor_class(name):
    if name == "ScientificReviewer":
        from processors.scientific_reviewer import ScientificReviewer
        return ScientificReviewer
    elif name == "Translator":
        from processors.translator import Translator
        return Translator
    elif name == "Reporter":
        from processors.reporter import Reporter
        return Reporter
    
    # GrammarReviewer as default processor, but unrecognised processors will throw an error
    elif name == "" or name == "GrammarReviewer":
        if (name == ""):
            print("No reviewer defined. Will default to Grammar reviewer")
        from processors.grammar_reviewer import GrammarReviewer
        return GrammarReviewer
    else:
        raise ValueError(f"Unrecognised processor type: {name}")

def main():
    args = parse_args()
    config = ConfigManager(args.config)
    config.override("io.input_directory", args.input_dir)
    config.override("io.output_directory", args.output_dir)
    if args.heading_styles:
        config.override("processing.heading_styles", args.heading_styles)
    if args.prompt:
        config.override("openai.prompt", args.prompt)
    if args.processor:
        config.override("processing.processor", args.processor)
    if args.severity is not None:
        config.override("processing.severity", args.severity)
    if args.source_lang:
        config.override("processing.source_lang", args.source_lang)
    if args.target_lang:
        config.override("processing.target_lang", args.target_lang)
    if args.output_format:
        config.override("processing.output_format", args.output_format)

    logging_level = config.get("logging.level", "INFO")
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

    input_dir = config.get("io.input_directory")
    output_dir = config.get("io.output_directory")
    ensure_directory(output_dir)
    supported_ext = config.get("io.supported_extensions", [".docx"])

    documents = find_documents(input_dir, supported_ext)
    if not documents:
        return

    parser = DocumentParser(
        heading_styles=config.get("processing.heading_styles"),
        min_word_threshold=config.get("processing.min_word_threshold", 2)
    )

    processor_name = config.get("processing.processor", "Reviewer")
    output_format = config.get("processing.output_format", "txt")

    processor_parameters = {
        'severity' : config.get("processing.severity", 3),
        'source_lang' : config.get("processing.source_lang", "en"),
        'target_lang' : config.get("processing.target_lang", "en")
    }

    api_key = config.get("openai.api_key")
    model = config.get("openai.model")
    max_retries = config.get("openai.max_retries", 3)

    ProcessorClass = load_processor_class(processor_name)
    if not ProcessorClass:
        return

    client = OpenAIClient(api_key, model, max_retries)
    processor = ProcessorClass(client, processor_parameters)

    for doc_path in documents:
        sections = parser.parse_document(doc_path)
        results = processor.process_sections(sections)
        base_name = os.path.splitext(os.path.basename(doc_path))[0]

        if output_format == "txt":
            if results:
                out_file = os.path.join(output_dir, f"{base_name}_{processor.output_suffix()}.txt")
                with open(out_file, 'w', encoding='utf-8') as f:
                    for i, r in enumerate(results):
                        f.write(f"Section {i+1}:\n")
                        f.write(r+"\n"+"="*40+"\n")
        else:
            out_file = os.path.join(output_dir, f"{base_name}_{processor.output_suffix()}.docx")
            processor.generate_docx(doc_path, sections, results, out_file)

if __name__ == "__main__":
    main()
