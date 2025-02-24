# Portable document format retrieval augmented generator (PDFRAG)

This program does the following:

1. Converts a folder of PDF documents to markdown. (done)
2. Creates a vector database of sentences embedding (a-la BERT) extracted from markdown files. (done)
3. Identifies a set of most relevant sentences from the PDF documents to the user prompt. (provisionally done, additional data cleaning may be required)
4. Injects the most relevant sentences into a generated large language model prompt to synthesize into a response to a user query. (not yet done)

## Installation

Coming soon...

## Usage

More details better instructions coming soon.

```bash
# converting a folder with PDFs into a folder of markdown files
python src/pdf2mdd.py pdfs mdd
# generating a sentence vector database folder out of the markdown files folder
python src/gen_vector_db.py mdd bib
# querying the sentence vector database folder for relevant entries (showcase, saves hits to test.csv)
python src/query_vector_db.py bib test.csv 'What are the sensory modalities that contribute to self-motion perception, gait, and balance function?'
```
