# Portable document format retrieval augmented generator (PDFRAG)

This program does the following:

1. Converts a folder of PDF documents to markdown. (done)
2. Creates a vector database of sentences embedding (a-la BERT) extracted from markdown files. (done)
3. Identifies a set of most relevant sentences from the PDF documents to the user prompt. (provisionally done, additional data cleaning may be required)
4. Injects the most relevant sentences into a generative large language model prompt to synthesize into a response to a user query. (done)

## Installation

On the Mac/Linux, simply run the scripts/install.sh script in the terminal or by double clicking on it.

On Windows, coming soon...

## Usage

The functionality of this program is split into a set of functions, which are contained within the "scripts" folder.

### pdfrag/scripts/upload_pdfs.sh

Opens a dialog for you to select a folder with PDFs to be moved to: pdfrag/pdfs

### pdfrag/scripts/update_db.sh

Runs the conversion from pdfrag/pdfs to markdown files in pdfrag/mdd, and subsequently embeds the sentences in the resulting markdown files into the vector database.

### pdfrag/scripts/query.sh

Receives a user query, then fetches top k sentences from the vector database, injects them as a context to a generator model (ChatGPT API by default), and has it generate a response with citation to original documents (as implemented in system.txt file).



