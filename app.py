from flask import Flask, render_template, request, send_file
import os
import spacy
import pdfplumber
import pytesseract
import pandas as pd
from docx import Document
from PIL import Image
import pytesseract

# Add this line at the top (or wherever you load pytesseract)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


app = Flask(__name__)
nlp = spacy.load("trained_invoice_ner")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/app')
def extractor():
    return render_template("app.html")

@app.route('/extract', methods=["POST"])
def extract():
    file = request.files['file']
    content = ""
    mime_type = file.content_type

    if mime_type == "text/plain":
        content = file.read().decode("utf-8")
    elif mime_type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            content = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        content = "\n".join([p.text for p in doc.paragraphs])
    elif mime_type == "text/csv":
        df = pd.read_csv(file)
        content = df.to_string()
    elif "image" in mime_type:
        image = Image.open(file)
        content = pytesseract.image_to_string(image)

    doc = nlp(content)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    return render_template("app.html", extracted_text=content, entities=entities, pdf_ready=True)

@app.route('/download_pdf')
def download_pdf():
    return send_file("output.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
