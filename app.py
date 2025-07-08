import os
import spacy
import pytesseract
import pdfplumber
import pandas as pd
import docx
from PIL import Image
from flask import Flask, request, render_template, jsonify

# Initialize Flask
app = Flask(__name__)
nlp = spacy.load("trained_invoice_ner")

def extract_text(file):
    content = ""
    mime_type = file.content_type

    if mime_type == "text/plain":
        content = file.read().decode("utf-8")

    elif mime_type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            content = "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        content = "\n".join(para.text for para in doc.paragraphs)

    elif mime_type == "text/csv":
        df = pd.read_csv(file)
        content = df.to_string()

    elif "image" in mime_type:
        image = Image.open(file)
        content = pytesseract.image_to_string(image)

    return content

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    entities = []
    if request.method == "POST":
        file = request.files.get("document")
        if file:
            extracted_text = extract_text(file)
            if extracted_text.strip():
                doc = nlp(extracted_text)
                entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    
    return render_template("index.html", extracted_text=extracted_text, entities=entities)

if __name__ == "__main__":
    app.run(debug=True)
