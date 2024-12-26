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
from document_archiver import DocumentArchiver

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--input-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--heading-styles", nargs="+")
    parser.add_argument("--prompt")
    parser.add_argument("--additional-prompt")
    parser.add_argument("--processor")
    parser.add_argument("--severity", type=int)
    parser.add_argument("--source-lang")
    parser.add_argument("--api-key")
    parser.add_argument("--target-lang")
    parser.add_argument("--output-format", choices=["txt","docx"])
    parser.add_argument("--add-section-title")

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
    elif name == "Summariser":
        from processors.summariser import Summariser
        return Summariser
    elif name == "CustomPromptProcessor":
        from processors.custom_prompt_processor import CustomPromptProcessor
        return CustomPromptProcessor
    
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

    api_key = args.api_key or config.get("openai.api_key")
    if not api_key or api_key in ["", "YOUR-OPENAI-API-KEY"]:
        raise ValueError("Valid API key not found. Provide it via CLI or in the YAML config.")
    config.override("openai.api_key", api_key)

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
    if args.additional_prompt:
        config.override("processing.additional_prompt", args.additional_prompt)
    if args.add_section_title:
        config.override("processing.add_section_title", args.add_section_title)

    logging_level = config.get("logging.level", "INFO")
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

    input_dir = config.get("io.input_directory")
    output_dir = config.get("io.output_directory")

    ensure_directory(output_dir)
    supported_ext = config.get("io.supported_extensions", [".docx", ".txt", ".md", ".pdf"])

    documents = find_documents(input_dir, supported_ext)
    if not documents:
        print(f"No documents found in the input dir {input_dir}")
        return

    add_section_title=config.get("processing.add_section_title", True)

    parser = DocumentParser(
        heading_styles=config.get("processing.heading_styles"),
        min_word_threshold=config.get("processing.min_word_threshold", 2)
    )

    processor_name = config.get("processing.processor", "Reviewer")
    output_format = config.get("processing.output_format", "txt")

    # Docx in docx mode: if user approves this, processed text will be saved in a formatted docx
    docx_in_docx_mode = False

    has_docx_input = any(os.path.splitext(doc)[1].lower() == ".docx" for doc in documents)
    has_pdf_input = any(os.path.splitext(doc)[1].lower() == ".pdf" for doc in documents)

    if output_format == "docx":
        if has_docx_input:
            logging.warning(
                "You have chosen .docx as output format and some input files are .docx already. "
                "This will try to recreate a file that's as loyal as possible to the original one, "
                "and may require time. For simpler outputs, chose txt as output format instead. "
            )
            docx_in_docx_mode = True

        if has_pdf_input:
            logging.warning(
                "One of the inputs is .pdf and output is .docx. Just fyi: this will NOT produce a .docx that's formatted as the .pdf"
            )

    processor_parameters = {
        'prompt' : config.get("prompt", ''),
        'additional_prompt' : config.get("additional_prompt", ''),
        'severity' : config.get("processing.severity", 3),
        'source_lang' : config.get("processing.source_lang", "en"),
        'target_lang' : config.get("processing.target_lang", "en"),
        'docx_in_docx_mode' : docx_in_docx_mode
    }

    api_key = config.get("openai.api_key")
    model = config.get("openai.model")
    max_retries = config.get("openai.max_retries", 3)

    ProcessorClass = load_processor_class(processor_name)
    if not ProcessorClass:
        return

    client = OpenAIClient(api_key, model, max_retries)
    processor = ProcessorClass(client, processor_parameters)
    print(f"Chosen processor class: {processor.__class__.__name__}")

    for doc_path in documents:
        print(f"Processing {doc_path}")
        sections = parser.parse_document(doc_path, docx_in_docx_mode=docx_in_docx_mode)
        results = processor.process_sections(sections)
        archiver = DocumentArchiver(output_dir, output_format, add_section_title, docx_in_docx_mode)
        archiver.archive_document(doc_path, sections, results, processor)

if __name__ == "__main__":
    main()
