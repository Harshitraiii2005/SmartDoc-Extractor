import os
import json
import csv
import spacy
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import NERDataPreparerConfig
from src.entity.artifact_entity import NERDataPreparerArtifact

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

class NERDataPreparer:
    def __init__(self, config: NERDataPreparerConfig):
        self.config = config
        self.nlp = spacy.blank("en")

    def generate_training_data(self) -> NERDataPreparerArtifact:
        clean_data = []
        misaligned_count = 0

        try:
            logging.info(f"📄 Reading from CSV: {self.config.csv_file}")
            with open(self.config.csv_file, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row_num, row in enumerate(reader, start=1):
                    file_name = row["Filename"]
                    txt_name = file_name.replace(".pdf", ".txt").replace(".PDF", ".txt")
                    text_path = os.path.join(self.config.text_dir, txt_name)

                    if not os.path.exists(text_path):
                        logging.warning(f"[{row_num}] Missing file: {text_path}")
                        continue

                    with open(text_path, encoding="utf-8") as f:
                        text = f.read()

                    doc = self.nlp(text)
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
                                    logging.warning(f"[{file_name}] Misaligned span: '{value}' → '{label}'")
                            else:
                                logging.warning(f"[{file_name}] Value not found: '{value}' → '{label}'")

                    if valid_entities:
                        clean_data.append((text, {"entities": valid_entities}))
                        logging.info(f"✅ {file_name}: {len(valid_entities)} entities")

        except Exception as e:
            logging.error("❌ Error during CSV or file reading", exc_info=True)
            raise CustomException(e)

        try:
            with open(self.config.output_json, "w", encoding="utf-8") as out:
                json.dump(clean_data, out, indent=2, ensure_ascii=False)

            logging.info(f"✅ Training data saved to: {self.config.output_json}")
            logging.info(f"⚠️ Total misaligned spans: {misaligned_count}")

            return NERDataPreparerArtifact(
                training_data_path=self.config.output_json,
                num_records=len(clean_data),
                status="Success"
            )

        except Exception as e:
            logging.error("❌ Failed to write output JSON", exc_info=True)
            raise CustomException(e)
