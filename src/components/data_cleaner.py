import os
import re
import unicodedata
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataCleanerConfig
from src.entity.artifact_entity import DataCleanerEntity

class DataCleaner:
    def __init__(self, config: DataCleanerConfig):
        self.config = config
        os.makedirs(self.config.output_dir, exist_ok=True)
        logging.info(f"📁 Output directory prepared: {self.config.output_dir}")

    def clean_text(self, text: str) -> str:
        try:
            # Remove unwanted page markers (e.g., ---- Page 1 ----)
            text = re.sub(r"-{2,}\s*Page\s*\d+\s*-{2,}", "", text)

            # Remove non-printable characters
            text = ''.join(c for c in text if c.isprintable())

            # Normalize Unicode text
            text = unicodedata.normalize("NFKC", text)

            # Fix hyphenated line breaks
            text = re.sub(r"-\n(\w+)", r"\1", text)

            # Merge lines while preserving double breaks
            lines = text.splitlines()
            merged_lines = []
            buffer = ""

            for line in lines:
                if line.strip() == "":
                    if buffer:
                        merged_lines.append(buffer.strip())
                        buffer = ""
                    merged_lines.append("")
                else:
                    buffer += " " + line.strip() if buffer else line.strip()

            if buffer:
                merged_lines.append(buffer.strip())

            text = "\n".join(merged_lines)

            # Clean extra spaces
            text = re.sub(r"[ \t]+", " ", text)

            # Standardize separators
            text = re.sub(r"\s*[-–]\s*", ": ", text)

            return text.strip()

        except Exception as e:
            logging.error("❌ Error in clean_text()", exc_info=True)
            raise CustomException(e)

    def clean_all_texts(self) -> DataCleanerEntity:
        try:
            logging.info(f"🧹 Starting OCR cleaning from: {self.config.input_dir}")

            for filename in os.listdir(self.config.input_dir):
                if filename.endswith(".txt"):
                    input_path = os.path.join(self.config.input_dir, filename)
                    with open(input_path, "r", encoding="utf-8") as f:
                        raw_text = f.read()

                    cleaned = self.clean_text(raw_text)

                    output_path = os.path.join(self.config.output_dir, filename)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(cleaned)

                    logging.info(f"✅ Cleaned text saved: {filename}")

            return DataCleanerEntity(
                cleaned_dir=self.config.output_dir,
                status="Success"
            )

        except Exception as e:
            logging.error("❌ Error during cleaning phase", exc_info=True)
            raise CustomException(e)
