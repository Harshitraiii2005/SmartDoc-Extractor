from src.components.ner_predictor import NERPredictor
from src.entity.config_entity import NERPredictorConfig

sample_text = """
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

config = NERPredictorConfig(model_path="trained_invoice_ner")
predictor = NERPredictor(config)
artifact = predictor.predict(sample_text)

# Display Results
print("\n🔍 Entities Detected:")
for ent, label in artifact.extracted_entities:
    print(f"{ent:<40} => {label}")

print("\n📋 Trained Labels:")
print(artifact.labels)
