import spacy
from spacy.training import Example
import json

# Load blank English NLP pipeline
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Load extracted field data
with open("extracted_fields_summary.json", encoding="utf-8") as f:
    raw_data = json.load(f)

# Field label mappings
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

# Clean overlapping entities
def remove_overlapping_entities(entities):
    # Sort by start index and longer span first
    entities = sorted(entities, key=lambda x: (x[0], -(x[1] - x[0])))
    result = []
    occupied = set()

    for start, end, label in entities:
        if not any(pos in occupied for pos in range(start, end)):
            result.append((start, end, label))
            occupied.update(range(start, end))
    return result

# Build training examples
TRAIN_DATA = []
labels = set()

for row in raw_data:
    text = row.get("Text", "")
    if not text:
        continue

    ents = []
    for field, label in FIELD_LABELS.items():
        value = row.get(field)
        if value and value.strip():
            value = value.strip()
            start = text.find(value)
            if start != -1:
                end = start + len(value)
                ents.append((start, end, label))

    ents = remove_overlapping_entities(ents)

    if ents:
        TRAIN_DATA.append({"text": text, "entities": ents})
        for _, _, label in ents:
            labels.add(label)

# Register labels
for label in labels:
    ner.add_label(label)

# Train
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for itn in range(30):
        print(f"\n📦 Iteration {itn + 1}")
        losses = {}
        for example in TRAIN_DATA:
            doc = nlp.make_doc(example["text"])
            ex = Example.from_dict(doc, {"entities": example["entities"]})
            nlp.update([ex], drop=0.3, sgd=optimizer, losses=losses)
        print("Loss:", losses)

# Save model
nlp.to_disk("trained_invoice_ner")
print("\n✅ Model saved to: trained_invoice_ner")
