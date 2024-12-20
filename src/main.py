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
    if name == "Reviewer":
        from processors.reviewer import Reviewer
        return Reviewer
    elif name == "ScientificReviewer":
        from processors.scientific_reviewer import ScientificReviewer
        return ScientificReviewer
    elif name == "Translator":
        from processors.translator import Translator
        return Translator
    return None

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

    api_key = config.get("openai.api_key")
    model = config.get("openai.model")
    max_retries = config.get("openai.max_retries", 3)
    processor_name = config.get("processing.processor", "Reviewer")
    severity = config.get("processing.severity", 3)
    source_lang = config.get("processing.source_lang", "en")
    target_lang = config.get("processing.target_lang", "en")
    output_format = config.get("processing.output_format", "txt")

    ProcessorClass = load_processor_class(processor_name)
    if not ProcessorClass:
        return

    client = OpenAIClient(api_key, model, max_retries)
    processor = ProcessorClass(client, severity, source_lang, target_lang)

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
