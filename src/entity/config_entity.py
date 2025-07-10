from dataclasses import dataclass
from typing import Optional


@dataclass
class DataExtractionEntity:
    input_dir: str                     
    output_dir: str                     


@dataclass
class FieldExtractionEntity:
    cleaned_text_dir: str              
    output_json_path: str              


@dataclass
class DataFeildGetterEntity:
    csv_file: str                      
    text_dir: str                     
    output_json: str                  


@dataclass
class TrainingDataValidatorConfig:
    input_json: str                    
    output_clean_json: str           


@dataclass
class NERTrainerConfig:
    training_data_path: str          
    model_output_dir: str            
    num_iterations: int = 30          


@dataclass
class NERPredictorConfig:
    model_path: str                   
