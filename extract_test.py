import os
from pdf2image import convert_from_path
import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Input and output directories
input_dir = 'data'
output_dir = 'extracted_texts'
os.makedirs(output_dir, exist_ok=True)

# Process each PDF
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        text_output = []

        print(f"Processing: {filename}")

        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=300)

        # OCR each page
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='eng')
            text_output.append(f"\n\n---- Page {i+1} ----\n{text}")

        # Save extracted text
        output_file = os.path.join(output_dir, filename.replace('.pdf', '.txt'))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(text_output))

        print(f"Extracted text saved to: {output_file}")
