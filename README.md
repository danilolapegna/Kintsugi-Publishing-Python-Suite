# Kintsugi Project AI tech stack
## Code for crafting and spreading high-quality knowledge

This project emerged from over a decade of self-publishing books on Amazon in multiple languages. Its purpose was to create a reliable AI-based framework for reviewing, translating, and analyzing my books across various formats. Quality has always been my top priority, and this system allowed me to ensure every book met the highest standards in clarity and precision.

What started as a personal solution evolved into a tool for producing and sharing high-quality knowledge on productivity, learning, lifehacking, and personal development. It streamlined my publishing process and opened up new possibilities for content creation and dissemination.

Note: this code can't AI-generate new books. I write all of my books myself. But can make your .docx documents much better, translate them in different languages, and much more!

![Book images](https://cdn.shopify.com/s/files/1/0273/6517/9457/files/Screenshot_2024-12-20_alle_17.36.17.png?v=1734712748)
[More info here](https://www.amazon.com/stores/Danilo-Lapegna/author/B0CGMF7CGG)

This project uses OpenAI’s API for language tasks, supports configurable prompts, and offers a plugin-based architecture for maximum extensibility and flexibility.

## Features
- Python + OpenAI-powered grammar reviewer, scientific reviewer, universal translator, and soon much more: put your .docx or .txt in the input folder, choose the functionality, and the script will send those documents, in sequence, to OpenAI for translation, review or anything you like.
- Supports multiple document formats (DOCX, PDF, TXT, MD).
- Customizable configuration via `config.yaml` or CLI arguments.
- Plugin-based architecture: easily add new functionalities like analytics and such.

## How this works, in short
- It will take all documents in the input folder
- Then will send each of them, one section at a time, to a processor class (usually an OpenAI api client) that will review/translate/summarise it.
- At the end, it will save the report for each document in a separate file or embed the results into a new, entirely formatted .docx file (WIP functionality).
- Can be used for batch document processing, document translations, document reviews, summarising and much more!
- **I personally used it in my project for:** fast high-quality translations, speeding up grammatical & factual reviews, and summarizing and filtering large quantities of data for research purposes. But you can use it for any workflow that involves processing and analyzing documents efficiently, tailoring it to your specific needs.

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


Override default heading styles (= what delimits a section in .docx files) directly from the CLI:
   ```bash
   python src/main.py --heading-styles "Heading 1" "Title"
   ```

## Future features and improvements

- Complete the in-docx embedded processor