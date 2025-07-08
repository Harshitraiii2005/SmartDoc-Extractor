from dataclasses import dataclass
from typing import Optional

# ---------- 1. Data Extraction ----------
@dataclass
class DataExtractionEntity:
    input_dir: str                      # Directory containing input PDFs
    output_dir: str                     # Directory to store extracted .txt files

# ---------- 2. Field Extraction ----------
@dataclass
class FieldExtractionEntity:
    cleaned_text_dir: str              # Directory with cleaned .txt files
    output_json_path: str              # Path to store extracted_fields_summary.json

# ---------- 3. Data Field to Span Alignment (Training JSON) ----------
@dataclass
class DataFeildGetterEntity:
    csv_file: str                      # Extracted field summary .csv
    text_dir: str                      # Cleaned .txt folder
    output_json: str                   # Output .json for SpaCy training (NER format)

# ---------- 4. Training Validator (Optional) ----------
@dataclass
class TrainingDataValidatorConfig:
    input_json: str                    # Extracted JSON
    output_clean_json: str            # Output clean JSON (after misalignment fix)

# ---------- 5. NER Training ----------
@dataclass
class NERTrainerConfig:
    training_data_path: str           # Path to training data JSON
    model_output_dir: str             # Output model folder
    num_iterations: int = 30          # Default to 30 iterations

# ---------- 6. NER Inference ----------
@dataclass
class NERPredictorConfig:
    model_path: str                   # Trained SpaCy model directory
