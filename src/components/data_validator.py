import spacy
import json
from spacy.training import offsets_to_biluo_tags, Example
from src.logger import logging
from src.exception import   MyException
from src.entity.config_entity import NERDataCleanerConfig
from src.entity.artifact_entity import NERDataCleanerArtifact

class NERDataCleaner:
    def __init__(self, config: NERDataCleanerConfig):
        self.config = config
        self.nlp = spacy.blank("en")

    def clean_data(self) -> NERDataCleanerArtifact:
        try:
            with open(self.config.input_json, encoding="utf-8") as f:
                data = json.load(f)

            total = len(data)
            logging.info(f"🔍 Loaded {total} raw NER records for validation")

            clean_data = []
            misaligned = 0
            conflicting = 0

            for i, item in enumerate(data):
                text = item.get("Text", "")
                doc = self.nlp.make_doc(text)

                entities = []
                for key, value in item.items():
                    if key in ["Filename", "Text"] or not value or value == "None":
                        continue
                    value = value.strip()
                    start = text.find(value)
                    if start != -1:
                        end = start + len(value)
                        entities.append((start, end, key.upper()))

                try:
                    tags = offsets_to_biluo_tags(doc, entities)
                    if "-" in tags:
                        logging.warning(f"⚠️ Misaligned entity at index {i}")
                        misaligned += 1
                        continue

                    Example.from_dict(doc, {"entities": entities})
                    clean_data.append((text, {"entities": entities}))

                except ValueError as e:
                    logging.warning(f"❌ Conflict in example {i}: {e}")
                    conflicting += 1

            with open(self.config.output_json, "w", encoding="utf-8") as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)

            logging.info(f"✅ Cleaned data saved to: {self.config.output_json}")
            logging.info(f"📊 Summary - Total: {total}, Clean: {len(clean_data)}, Misaligned: {misaligned}, Conflicting: {conflicting}")

            return NERDataCleanerArtifact(
                cleaned_data_path=self.config.output_json,
                clean_count=len(clean_data),
                misaligned_count=misaligned,
                conflict_count=conflicting,
                status="Success"
            )

        except Exception as e:
            logging.error("❌ Error in NERDataCleaner", exc_info=True)
            raise CustomException(e)
