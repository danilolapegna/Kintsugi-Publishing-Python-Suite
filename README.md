# Kintsugi Project tech stack: Code for crafting and spread high-quality knowledge!

This project I created served my self-publishing project. In fact its goal was provide me with a robust framework for reviewing, translating, and analyzing my writing in various formats, so that I could analyze, review, translate my books. And yeah, that means having additional tools for spreading high-quality knowledge on productivity, learning, lifehacking and personal development. 


![Book images](https://cdn.shopify.com/s/files/1/0273/6517/9457/files/Screenshot_2024-12-20_alle_17.36.17.png?v=1734712748)
[More info here](https://www.amazon.com/stores/Danilo-Lapegna/author/B0CGMF7CGG)

This project uses OpenAI’s API for language tasks, supports configurable prompts, and offers a plugin-based architecture for maximum extensibility and flexibility.

## Features

- Modularized code with clear separation of concerns.
- Supports multiple document formats (DOCX, TXT, MD).
- Customizable configuration via `config.yaml` or CLI arguments.
- Plugin-based architecture: easily add new functionalities like analytics and such.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Remember to add your OpenAI Api Key in config.yaml where now you have YOUR-OPENAI-API-KEY

3. Get ready to spread high-quality knowledge!

## Examples with using different processors

Use the ScientificReviewer in order to make (with OpenAI, model described in config.yaml) a scientific review of all the docx in the input folder. Set a high severity level:
   ```bash
   python src/main.py --processor ScientificReviewer --severity 5
   ```

Use the Translator processor to translate (with OpenAI, model described in config.yaml) all the docx in the input folder from Italian to English:

   ```bash
   python src/main.py --processor Translator --source-lang it --target-lang en
   ```

Output results in .docx format instead of .txt:

   ```bash
   python src/main.py --output-format docx
   ```

Use the Reviewer module, with low severity, use custom input/output directories, and generate .docx output in order to do a grammatical review of all documents:

   ```bash
   python src/main.py \
      --processor Reviewer \
       --severity 1 \
       --input-dir ./my_input_documents \
       --output-dir ./my_review_results \
      --output-format docx
   ```


Override default heading styles directly from the CLI:
   ```bash
   python src/main.py --heading-styles "Heading 1" "Title"
   ```