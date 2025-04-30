# Portable document format retrieval augmented generator (PDFRAG)

This program does the following:

1. Converts a folder of PDF documents to markdown. (done)
2. Creates a vector database of sentences embedding (a-la BERT) extracted from markdown files. (done)
3. Identifies a set of most relevant sentences from the PDF documents to the user prompt. (provisionally done, additional data cleaning may be required)
4. Injects the most relevant sentences into a generative large language model prompt to synthesize into a response to a user query. (done)

## Installation

### MacOS

After unzipping the program folder, simply right click on the install.command file, press open, and press ok on the warning message (I am a trusted developer lol). This will install the Homebrew package manager (if not already installed), and set up proper version of Python (for the main program) and zenity (for the limited GUI elements).

### Windows

Coming soon...

## Usage

### MacOS

The first time you run it, right click and then press open and press ok on warning. On subsequent attempts, can double click.

### Windows 

Coming soon...

## --- may be obsolete ---

The functionality of this program is split into a set of functions, which are contained within the "scripts" folder. To run the scripts, the recommended approach is to do it thru the terminal, from the main program directory:

```bash
cd pdfrag-main
./scripts/upload_pdfs.sh # to batch upload a folder of PDFs to the pdfrag/pdfs
./scripts/update_db.sh # generate MDD files and embed sentences into the vector database
./scripts/query.sh # run the query
```

### pdfrag/scripts/upload_pdfs.sh

Opens a dialog for you to select a folder with PDFs to be moved to: pdfrag/pdfs

### pdfrag/scripts/update_db.sh

Runs the conversion from pdfrag/pdfs to markdown files in pdfrag/mdd, and subsequently embeds the sentences in the resulting markdown files into the vector database.

### pdfrag/scripts/query.sh

Receives a user query, then fetches top k sentences from the vector database, injects them as a context to a generator model (ChatGPT API by default), and has it generate a response with citation to original documents (as implemented in system.txt file).



