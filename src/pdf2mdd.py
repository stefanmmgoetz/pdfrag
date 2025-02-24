#!/usr/bin/env python

import pymupdf4llm
from sys import argv
from pathlib import Path
from glob import glob
from tqdm import tqdm

def main(pdfdir: str, mddir: str):
    pdfs = glob(pdfdir+'/*.pdf')
    for pdf in tqdm(pdfs):
        md_file = pdf.replace('.pdf', '.md').replace(pdfdir, mddir)
        if not Path(md_file).exists():
            md_text = pymupdf4llm.to_markdown(pdf)
            Path(md_file).write_bytes(md_text.encode())

if __name__ == '__main__':
    pdfdir, mddir = argv[1], argv[2]
    if not Path(mddir).exists():
        Path(mddir).mkdir()
    main(pdfdir, mddir)