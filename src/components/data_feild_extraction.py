import os
import re
import json
import spacy
from typing import Dict
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataFeildGetterEntity
from src.entity.artifact_entity import DataFeildGetterArtifact

class FieldExtractor:
    def __init__(self, config: DataFeildGetterEntity):
        self.config = config
        os.makedirs(self.config.output_dir, exist_ok=True)
        self.nlp = spacy.load("en_core_web_sm")
        logging.info("🔍 SpaCy model loaded for NER field extraction")

    def extract_fields(self, text: str) -> Dict:
        try:
            doc = self.nlp(text)

            fields = {
                "Organizations": set(),
                "Persons": set(),
                "Addresses": set(),
                "Dates": set(),
                "Amounts": set(),
            }

            for ent in doc.ents:
                if ent.label_ == "ORG":
                    fields["Organizations"].add(ent.text)
                elif ent.label_ == "PERSON":
                    fields["Persons"].add(ent.text)
                elif ent.label_ == "GPE":
                    fields["Addresses"].add(ent.text)
                elif ent.label_ == "DATE":
                    fields["Dates"].add(ent.text)
                elif ent.label_ == "MONEY":
                    fields["Amounts"].add(ent.text)

            
            regex_patterns = {
                "Invoice Number": r"(Invoice No|Invoice #|Invoice ID|Invoice Ref|Inv No|Document No|Receipt No|Bill No)[^\n:]*[:]\s*([A-Z0-9\-/]+)",
                "Revision Number": r"(Revision No|Revision Number|Version)[^\n:]*[:]\s*(.+)",
                "Reference Number": r"(Reference No|Ref No|Reference Number)[^\n:]*[:]\s*([A-Z0-9\-]+)",
                "PO Number": r"(PO Number|Purchase Order|Order No|Order Number)[^\n:]*[:]\s*(.+)",
                "Challan Number": r"(Challan No|Challan Number|Challan ID)[^\n:]*[:]\s*(.+)",
                "Dispatch Document No": r"(Dispatch Document No|Dispatch Doc No|Dispatch Ref)[^\n:]*[:]\s*(.+)",
                "Delivery Note": r"(Delivery Note|Delivery Challan)[^\n:]*[:]\s*(.+)",
                "LR Number": r"(LR No|Lorry Receipt No|LR Number)[^\n:]*[:]\s*(.+)",
                "HSN Code": r"(HSN Code|HS Code|SAC Code)[^\n:]*[:]\s*([A-Z0-9]+)",
                "Issue Date": r"(Issue Date|Invoice Date|Date of Issue)[^\n:]*[:]\s*(.+)",
                "Due Date": r"(Due Date|Payment Due|Expiry Date)[^\n:]*[:]\s*(.+)",
                "Delivery Date": r"(Delivery Date|Dispatch Date)[^\n:]*[:]\s*(.+)",
                "Bill From": r"(From|Seller|Supplier|Issued By)[^\n:]*[:]\s*(.+)",
                "Bill To": r"(To|Buyer|Customer|Client|Purchaser|Billed To)[^\n:]*[:]\s*(.+)",
                "Shipping Address": r"(Ship To|Delivery Address|Dispatch Address|Consignee)[^\n:]*[:]\s*(.+)",
                "Authorized Signatory": r"(Authorized Signatory|Authorized Person)[^\n:]*[:]\s*(.+)",
                "Contact Email": r"(Email|E-mail|Email ID|Contact Email)[^\n:]*[:]\s*([\w\.-]+@[\w\.-]+)",
                "Contact Phone": r"(Phone|Mobile|Tel|Telephone|Contact No)[^\n:]*[:]\s*([0-9\-\+ ]+)",
                "GST Number": r"(GST No|GSTIN|GST Number|GST Registration)[^\n:]*[:]\s*([0-9A-Z]+)",
                "PAN Number": r"(PAN No|PAN Number|PAN)[^\n:]*[:]\s*([A-Z0-9]+)",
                "VAT Number": r"(VAT No|VAT Number)[^\n:]*[:]\s*([A-Z0-9]+)",
                "Service Tax Number": r"(Service Tax No|Service Tax Number)[^\n:]*[:]\s*([A-Z0-9]+)",
                "Vehicle Number": r"(Vehicle No|Vehicle Number|Truck No|Truck Number)[^\n:]*[:]\s*([A-Z0-9\-]+)",
                "Transporter Name": r"(Transporter Name|Carrier Name|Logistics Partner)[^\n:]*[:]\s*(.+)",
                "E-way Bill No": r"(E[- ]?Way Bill No|Eway Bill Number)[^\n:]*[:]\s*([A-Z0-9\-]+)",
                "Payment Terms": r"(Payment Terms|Terms of Payment)[^\n:]*[:]\s*(.+)",
                "Payment Info": r"(Payment Method|Payment Mode|Payment Type|Terms)[^\n:]*[:]\s*(.+)",
                "Currency": r"(Currency|Curr)[^\n:]*[:]\s*(\w+)",
                "Total Amount": r"(Total Amount|Grand Total|Amount Due|Total|Net Total|Payable Amount)[^\n:]*[:]\s*\$?([0-9\.,]+)",
                "Tax Amount": r"(Tax|GST|VAT|IGST|CGST|SGST|Service Tax)[^\n:]*[:]\s*\$?([0-9\.,]+)",
                "Advance Payment": r"(Advance Paid|Advance Payment)[^\n:]*[:]\s*\$?([0-9\.,]+)",
                "Balance Due": r"(Balance Due|Amount Due)[^\n:]*[:]\s*\$?([0-9\.,]+)",
                "Amount in Words": r"(Amount in Words)[^\n:]*[:]\s*(.+)",
                "Bank Account": r"(Account No|Bank Account No|A/c No|Account Number)[^\n:]*[:]\s*([A-Z0-9\- ]+)",
                "IFSC Code": r"(IFSC Code|Bank IFSC)[^\n:]*[:]\s*([A-Z0-9]+)",
                "SWIFT Code": r"(SWIFT Code|SWIFT)[^\n:]*[:]\s*([A-Z0-9]+)",
                "IBAN": r"(IBAN|IBAN Number)[^\n:]*[:]\s*([A-Z0-9]+)",
                "Country of Origin": r"(Country of Origin)[^\n:]*[:]\s*(.+)",
                "Country of Destination": r"(Country of Destination|Destination Country)[^\n:]*[:]\s*(.+)",
                "Port of Loading": r"(Port of Loading)[^\n:]*[:]\s*(.+)",
                "Port of Discharge": r"(Port of Discharge)[^\n:]*[:]\s*(.+)",
                "Remarks": r"(Remarks|Notes|Additional Information)[^\n:]*[:]\s*(.+)",
                "Terms and Conditions": r"(Terms and Conditions|Conditions)[^\n:]*[:]\s*(.+)"
            }

            for field, pattern in regex_patterns.items():
                match = re.search(pattern, text, re.I)
                fields[field] = match.group(len(match.groups())) if match else None

            
            for key in fields:
                if isinstance(fields[key], set):
                    fields[key] = ", ".join(fields[key]) if fields[key] else None

            return fields

        except Exception as e:
            logging.error("❌ Error in extract_fields()", exc_info=True)
            raise CustomException(e)

    def extract_fields_from_all(self) -> DataFeildGetterArtifact:
        try:
            all_data = []
            logging.info(f"📁 Extracting fields from cleaned texts in: {self.config.input_dir}")

            for filename in os.listdir(self.config.input_dir):
                if filename.endswith(".txt"):
                    file_path = os.path.join(self.config.input_dir, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    fields = self.extract_fields(text)
                    fields["Filename"] = filename
                    fields["Text"] = text
                    all_data.append(fields)

                    logging.info(f"✅ Fields extracted from: {filename}")

            output_json = os.path.join(self.config.output_dir, "extracted_fields_summary.json")
            with open(output_json, "w", encoding="utf-8") as jsonfile:
                json.dump(all_data, jsonfile, indent=2, ensure_ascii=False)

            logging.info(f"📦 Saved all extracted fields to: {output_json}")

            return DataFeildGetterArtifact(
                output_json_path=output_json,
                extracted_data=all_data,
                status="Success"
            )

        except Exception as e:
            logging.error("❌ Field extraction failed", exc_info=True)
            raise CustomException(e)
