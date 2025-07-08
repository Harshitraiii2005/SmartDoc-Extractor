import os
import re
import unicodedata

# Input and output directories
input_dir = 'extracted_texts'
output_dir = 'cleaned_texts'
os.makedirs(output_dir, exist_ok=True)

# Function to clean text
def clean_ocr_text(text):
    # Remove page markers
    text = re.sub(r"-{2,}\s*Page\s*\d+\s*-{2,}", "", text)

    # Remove non-printable characters
    text = ''.join(c for c in text if c.isprintable())

    # Normalize Unicode
    text = unicodedata.normalize("NFKC", text)

    # Fix hyphenation across lines
    text = re.sub(r"-\n(\w+)", r"\1", text)

    # Merge broken lines (but preserve double line breaks as paragraph breaks)
    lines = text.splitlines()
    merged_lines = []
    buffer = ""
    for line in lines:
        if line.strip() == "":
            if buffer:
                merged_lines.append(buffer.strip())
                buffer = ""
            merged_lines.append("")  # Keep paragraph breaks
        else:
            if buffer:
                buffer += " " + line.strip()
            else:
                buffer = line.strip()
    if buffer:
        merged_lines.append(buffer.strip())

    text = "\n".join(merged_lines)

    # Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Standardize separators: convert - and – to :
    text = re.sub(r"\s*[-–]\s*", ": ", text)

    # Final trimming
    text = text.strip()

    return text

# Process all files
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_dir, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = clean_ocr_text(raw_text)

        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Cleaned: {filename}")
