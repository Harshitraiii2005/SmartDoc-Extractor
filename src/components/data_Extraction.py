import os
from pdf2image import convert_from_path
import pytesseract
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataExtractionEntity
from src.entity.artifact_entity import DataExtractionArtifact

class DataExtractor:
    def __init__(self, config: DataExtractionEntity):
        self.config = config
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        logging.info("🔧 Tesseract path set successfully.")

    def extract_text_from_pdfs(self) -> DataExtractionArtifact:
        try:
            logging.info(f"📂 Starting PDF extraction from: {self.config.input_dir}")

            for filename in os.listdir(self.config.input_dir):
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(self.config.input_dir, filename)
                    text_output = []

                    logging.info(f"📄 Processing file: {filename}")
                    images = convert_from_path(pdf_path, dpi=300)

                    for i, image in enumerate(images):
                        text = pytesseract.image_to_string(image, lang="eng")
                        text_output.append(f"\n\n---- Page {i+1} ----\n{text}")

                    output_file = os.path.join(self.config.output_dir, filename.replace(".pdf", ".txt"))
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write("\n".join(text_output))

                    logging.info(f"✅ Text saved to: {output_file}")

            logging.info("🎉 Text extraction completed successfully.")
            return DataExtractionArtifact(
                extracted_dir=self.config.output_dir,
                status="Success"
            )

        except Exception as e:
            logging.error("❌ Exception during text extraction", exc_info=True)
            raise CustomException(e)
