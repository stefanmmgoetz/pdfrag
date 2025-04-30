#!/usr/bin/env python

import pymupdf4llm
from sys import argv
from pathlib import Path
from glob import glob
from tqdm import tqdm
import ocrmypdf
import logging
import fitz
import io

logging.getLogger().setLevel(logging.INFO)

def get_prop_ascii(string: str):
    string_length = len(string)
    ascii_count = sum([c.isascii() for c in string])
    return ascii_count / string_length

def get_prop_alnum(string: str):
    string_length = len(string)
    alnum_count = sum([c.isalnum() for c in string])
    return alnum_count / string_length

def ocr_fallback(pdf: str):
    ocrpdf = io.BytesIO()
    ocrmypdf.ocr(pdf, ocrpdf, force_ocr=True, output_type='pdf')
    doc = fitz.open('pdf', ocrpdf)
    doc_string = ''
    for page in doc:
        doc_string += page.get_text()
    return doc_string

def pdf2mdd(pdf: str):
    md_text = pymupdf4llm.to_markdown(pdf)
    prop_ascii = get_prop_ascii(md_text)
    prop_alnum = get_prop_alnum(md_text)
    logging.info('ascii proportion: ' + str(prop_ascii))
    logging.info('alphanumeric proportion: ' + str(prop_alnum))
    if prop_ascii < 0.5 or prop_alnum < 0.5:
        logging.warning('pymupdf4llm conversion failed')
        logging.warning('Falling back on OCR-based text extraction.')
        md_text = ocr_fallback(pdf)
    return md_text

def main(pdfdir: str, mddir: str):
    pdfs = glob(pdfdir+'/*.pdf')
    for pdf in tqdm(pdfs):
        md_file = pdf.replace('.pdf', '.md').replace(pdfdir, mddir)
        if not Path(md_file).exists():
            md_text = pdf2mdd(pdf)
            Path(md_file).write_bytes(md_text.encode())

if __name__ == '__main__':
    pdfdir, mddir = argv[1], argv[2]
    if not Path(mddir).exists():
        Path(mddir).mkdir()
    main(pdfdir, mddir)