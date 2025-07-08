import csv
import json
import os
import spacy

# Paths
CSV_FILE = "extracted_fields_summary.csv"
TEXT_DIR = "extracted_texts"
OUTPUT_JSON = "ner_training_data_clean.json"

# Load blank spaCy pipeline
nlp = spacy.blank("en")

# Field to label mapping
FIELD_LABELS = {
    "Invoice Number": "INVOICE_NUMBER",
    "Revision Number": "REVISION_NUMBER",
    "Reference Number": "REFERENCE_NUMBER",
    "PO Number": "PO_NUMBER",
    "Challan Number": "CHALLAN_NUMBER",
    "Dispatch Document No": "DISPATCH_DOCUMENT",
    "Delivery Note": "DELIVERY_NOTE",
    "LR Number": "LR_NUMBER",
    "HSN Code": "HSN_CODE",
    "Issue Date": "ISSUE_DATE",
    "Due Date": "DUE_DATE",
    "Delivery Date": "DELIVERY_DATE",
    "Bill From": "SELLER",
    "Bill To": "BUYER",
    "Shipping Address": "SHIP_ADDRESS",
    "Authorized Signatory": "SIGNATORY",
    "Contact Email": "EMAIL",
    "Contact Phone": "PHONE",
    "GST Number": "GSTIN",
    "PAN Number": "PAN",
    "VAT Number": "VAT",
    "Service Tax Number": "SERVICE_TAX",
    "Vehicle Number": "VEHICLE_NUMBER",
    "Transporter Name": "TRANSPORTER",
    "E-way Bill No": "EWAY_BILL",
    "Payment Terms": "PAYMENT_TERMS",
    "Payment Info": "PAYMENT_INFO",
    "Currency": "CURRENCY",
    "Total Amount": "TOTAL_AMOUNT",
    "Tax Amount": "TAX_AMOUNT",
    "Advance Payment": "ADVANCE_PAYMENT",
    "Balance Due": "BALANCE_DUE",
    "Amount in Words": "AMOUNT_IN_WORDS",
    "Bank Account": "BANK_ACCOUNT",
    "IFSC Code": "IFSC",
    "SWIFT Code": "SWIFT",
    "IBAN": "IBAN",
    "Country of Origin": "ORIGIN_COUNTRY",
    "Country of Destination": "DEST_COUNTRY",
    "Port of Loading": "PORT_LOADING",
    "Port of Discharge": "PORT_DISCHARGE",
    "Remarks": "REMARKS",
    "Terms and Conditions": "TERMS_AND_CONDITIONS"
}

clean_data = []
misaligned_count = 0

with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row_num, row in enumerate(reader):
        file_name = row["Filename"]
        text_path = os.path.join(TEXT_DIR, file_name.replace(".pdf", ".txt").replace(".PDF", ".txt"))
        if not os.path.exists(text_path):
            print(f"⚠️ Skipping missing text: {text_path}")
            continue

        with open(text_path, encoding="utf-8") as f:
            text = f.read()

        doc = nlp(text)
        valid_entities = []

        for field, label in FIELD_LABELS.items():
            value = row.get(field)
            if value and value.strip() and value != "None":
                value = value.strip()
                start = text.find(value)
                if start != -1:
                    end = start + len(value)
                    span = doc.char_span(start, end, label=label, alignment_mode="contract")
                    if span:
                        valid_entities.append((span.start_char, span.end_char, label))
                    else:
                        misaligned_count += 1
                        print(f"⚠️ Misaligned span in {file_name} for '{value}' as '{label}'")
                else:
                    print(f"❌ Value '{value}' for label '{label}' not found in '{file_name}'.")

        if valid_entities:
            clean_data.append((text, {"entities": valid_entities}))

# Save clean data
with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
    json.dump(clean_data, out, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(clean_data)} clean examples to {OUTPUT_JSON}")
print(f"⚠️ Skipped {misaligned_count} misaligned entity spans\n")
