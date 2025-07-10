from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
EXTRACTED_TEXT_DIR = ROOT_DIR / "extracted_texts"
CLEANED_TEXT_DIR = ROOT_DIR / "cleaned_texts"
TRAINED_MODEL_DIR = ROOT_DIR / "trained_invoice_ner"


EXTRACTED_FIELDS_JSON = ROOT_DIR / "extracted_fields_summary.json"
NER_TRAINING_DATA_JSON = ROOT_DIR / "ner_training_data_clean.json"
EXTRACTED_FIELDS_CSV = ROOT_DIR / "extracted_fields_summary.csv"
TEST_PREDICTION_JSON = ROOT_DIR / "extracted_texts" / "fields.json"


SUPPORTED_FILE_TYPES = [".txt", ".pdf", ".docx", ".csv", ".jpg", ".jpeg", ".png"]


TRAINING_ITERATIONS = 30
DROPOUT_RATE = 0.3
