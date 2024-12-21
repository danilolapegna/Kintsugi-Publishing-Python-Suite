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
- Supports multiple document formats (DOCX, TXT, MD).
- Customizable configuration via `config.yaml` or CLI arguments.
- Plugin-based architecture: easily add new functionalities like analytics and such.
- For all code geeks: Modularized code with clear separation of concerns.

## A bit more detail on how it works, in case you're interested

The script processes documents (Word, text, or Markdown) by breaking them into meaningful sections based on headings or content. Each section is then sent to OpenAI, where it can be translated, improved, or analyzed according to the chosen functionality. Finally, each result is appended and saved into a txt file or embedded into a new .docx file (functionality in development). Short, uninformative sections are also automatically merged to ensure each request is substantial enough for the model.

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

## Future features and improvements

- Complete the in-docx processor
- The fact that processors are all a bit different from each other may defy the need for such inheritance, but this can be refactored later