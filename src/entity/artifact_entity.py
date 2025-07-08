from dataclasses import dataclass
from typing import List, Tuple, Optional

# ---------- 1. Data Extraction ----------
@dataclass
class DataExtractionArtifact:
    extracted_dir: str                # Path to folder with .txt files
    status: str                       # Success or Error

# ---------- 2. Field Extraction ----------
@dataclass
class FieldExtractionArtifact:
    json_path: str                    # Path to extracted_fields_summary.json
    status: str

# ---------- 3. Span Aligned JSON Output ----------
@dataclass
class DataFeildGetterArtifact:
    output_json_path: str             # Cleaned JSON with spans
    total_records: int
    misaligned: int
    status: str

# ---------- 4. Validator (Optional) ----------
@dataclass
class TrainingValidatorArtifact:
    cleaned_data_path: str
    valid_count: int
    misaligned_count: int
    conflicting_count: int

# ---------- 5. NER Training ----------
@dataclass
class NERTrainerArtifact:
    model_path: str
    training_loss: List[float]
    status: str

# ---------- 6. NER Prediction ----------
@dataclass
class NERPredictorArtifact:
    input_text: str
    extracted_entities: List[Tuple[str, str]]  # (EntityText, Label)
    labels: List[str]
    status: str
