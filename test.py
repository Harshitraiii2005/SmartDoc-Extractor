import spacy
import sys

# Load the trained NER model
MODEL_PATH = "trained_invoice_ner"
nlp = spacy.load(MODEL_PATH)

# Sample test text (You can replace this or read from a file using sys.argv)
test_text = """
GST TAX INVOICE

Invoice No: INV-1040
Date: 31 May 2025

Supplier:
Davis, Thompson and Martin
2545 Abigail Mission Smithborough, GU 06171
GSTIN: 497064490705
Contact: 750-288-7740

Buyer:
Barnett Ltd
5385 Butler Street Apt. 942 Kimberlyton, DE 45355
GSTIN: 665461734208
Contact: 001-645-436-2864x562

Place of Supply: Catherineberg

PO Number: PO-5240
Amount Paid: $1528.61
Payment Info: Net Banking
"""

# Optional: Load text from file if given as command-line argument
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    with open(filepath, encoding="utf-8") as f:
        test_text = f.read()
    print(f"\n📄 Testing on: {filepath}")

# Run the model
doc = nlp(test_text)

# Print results
print("\n🔍 Detected Entities:\n")
for ent in doc.ents:
    print(f"{ent.text.strip():<40} => {ent.label_}")

print("\n📋 Labels this model was trained to detect:")
print(nlp.get_pipe("ner").labels)
