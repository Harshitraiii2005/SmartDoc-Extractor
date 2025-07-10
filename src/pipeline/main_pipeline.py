import os
from src.logger import logging
from src.exception import CustomException


from src.components.data_Extraction import DataExtractor
from src.components.data_cleaner import DataCleaner
from src.components.data_feild_extraction import FieldExtractor
from src.components.data_prepare import NERDataPreparer
from src.components.data_trainer import NERTrainer



from src.entity.config_entity import (
    DataExtractionEntity,
    FieldExtractionEntity,
    DataFeildGetterEntity,
    NERTrainerConfig,
    NERPredictorConfig
)


def run_pipeline():
    try:
        logging.info("🚀 Starting SmartDoc-Extractor Pipeline...")

        
        extraction_config = DataExtractionEntity(
            input_dir="data",
            output_dir="artifacts/extracted_texts"
        )
        extractor = DataExtractor(config=extraction_config)
        extraction_artifact = extractor.extract_text_from_pdfs()

        
        cleaner = DataCleaner(extraction_artifact)
        cleaner.clean()  

        
        field_config = FieldExtractionEntity(
            cleaned_text_dir=extraction_artifact.extracted_dir,
            output_json_path="artifacts/extracted_fields_summary.json"
        )
        field_extractor = FieldExtractor(config=field_config)
        field_artifact = field_extractor.extract_fields_from_texts()

        
        train_data_config = DataFeildGetterEntity(
            csv_file="artifacts/extracted_fields_summary.csv",
            text_dir=extraction_artifact.extracted_dir,
            output_json="artifacts/ner_training_data_clean.json"
        )
        data_preparer = NERDataPreparer(config=train_data_config)
        training_artifact = data_preparer.generate_clean_training_data()

        
        trainer_config = NERTrainerConfig(
            training_data_path=training_artifact.output_json_path,
            model_output_dir="artifacts/trained_invoice_ner",
            num_iterations=30
        )
        trainer = NERTrainer(config=trainer_config)
        trainer_artifact = trainer.train_model()

        
        predictor_config = NERPredictorConfig(
            model_path=trainer_artifact.model_path
        )
        predictor = NERPredictor(config=predictor_config)
        predictor.predict_on_sample()

        logging.info("✅ SmartDoc-Extractor Pipeline Execution Complete!")

    except Exception as e:
        logging.error("❌ Pipeline failed!", exc_info=True)
        raise CustomException(e)



if __name__ == "__main__":
    run_pipeline()
