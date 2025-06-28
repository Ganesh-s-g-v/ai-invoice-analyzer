# Invoice Analyzer Bot

An AI-powered web app to extract key information (total amount, date, invoice number) from uploaded invoice images or PDFs using OCR.

## Features
- Upload invoice (image or PDF)
- Extracts total amount, date, and invoice number using OCR and regex
- Displays results in a clean Bootstrap UI
- Shows raw OCR output for reference

## Tech Stack
- Flask (backend)
- Bootstrap 5 (frontend)
- pytesseract (OCR)
- Pillow (image handling)
- pdf2image (PDF to image conversion)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Tesseract OCR engine (see https://github.com/tesseract-ocr/tesseract)
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser.

## Project Structure
```
invoice-analyzer/
├── app.py
├── templates/
│   ├── index.html
│   └── result.html
├── uploads/
├── requirements.txt
└── README.md
``` 