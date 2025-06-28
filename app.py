# app.py (Updated to use working Gemini SDK approach for invoices)
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
import json, re

# Configure Tesseract for OCR (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Gemini setup (SDK-based)
GEMINI_API_KEY = "AIzaSyAgWCSBm2igEQP3fodIQNcflY9qur7ivqQ"  # Use your API key
genai.configure(api_key=GEMINI_API_KEY)

# Allowed file types

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Gemini invoice analysis using inline base64 and SDK
def analyze_invoice_with_gemini_base64(encoded_file, mime_type):
    prompt = """
    You're a friendly, conversational assistant who summarizes invoices in a simple and chatty way.
    When given an invoice file, reply as if you're speaking to a person who wants a quick rundown.
    The tone should be casual, helpful, and personal. Make sure it feels like a human message.
    Include the following key points in your explanation:
    - Who the invoice is from (company or sender)
    - Date of the invoice
    - Purpose or description of the invoice
    - Total amount due
    - Invoice number

    Use emojis lightly (if appropriate), keep it short and friendly.
    Here's an example:
    "Hey! 👋 This invoice is from ABC Corp, dated May 4. It’s for website hosting services and the total is $89.99. Invoice number is #4567."
    """
    model = genai.GenerativeModel('gemini-2.5-flash')  # ✅ CORRECTED
    response = model.generate_content([
        {
            "inline_data": {
                "mime_type": mime_type,
                "data": encoded_file
            }
        },
        {
            "text": prompt
        }
    ])
    return {"summary": response.text.strip()}


@app.route('/list_models')
def list_models():
    models = genai.list_models()
    return f"<pre>{models}</pre>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'invoice' not in request.files:
        flash('No file uploaded.')
        return redirect(url_for('index'))

    file = request.files['invoice']
    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            mime_type = "application/pdf" if filename.lower().endswith(".pdf") else "image/jpeg"

            result = analyze_invoice_with_gemini_base64(encoded_file, mime_type)
            return render_template('result.html', fields=result, ocr_text="(Gemini used for full file analysis)")

        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Upload PNG, JPG, JPEG, or PDF.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
