from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class DataExtractionArtifact:
    extracted_dir: str               
    status: str                       


@dataclass
class FieldExtractionArtifact:
    json_path: str                   
    status: str


@dataclass
class DataFeildGetterArtifact:
    output_json_path: str             
    total_records: int
    misaligned: int
    status: str


@dataclass
class TrainingValidatorArtifact:
    cleaned_data_path: str
    valid_count: int
    misaligned_count: int
    conflicting_count: int


@dataclass
class NERTrainerArtifact:
    model_path: str
    training_loss: List[float]
    status: str


@dataclass
class NERPredictorArtifact:
    input_text: str
    extracted_entities: List[Tuple[str, str]]  
    labels: List[str]
    status: str
