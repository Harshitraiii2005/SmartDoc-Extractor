import spacy
import json
from spacy.training import Example
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import NERTrainerConfig
from src.entity.artifact_entity import NERTrainerArtifact


class NERTrainer:
    def __init__(self, config: NERTrainerConfig):
        self.config = config
        self.nlp = spacy.blank("en")
        self.ner = self.nlp.add_pipe("ner")

    def remove_overlapping_entities(self, entities):
        entities = sorted(entities, key=lambda x: (x[0], -(x[1] - x[0])))
        result = []
        occupied = set()

        for start, end, label in entities:
            if not any(pos in occupied for pos in range(start, end)):
                result.append((start, end, label))
                occupied.update(range(start, end))
        return result

    def load_data(self):
        try:
            with open(self.config.training_data_path, encoding="utf-8") as f:
                data = json.load(f)

            train_data = []
            label_set = set()

            for row in data:
                text = row.get("Text", "")
                if not text:
                    continue

                ents = []
                for field, label in self.config.label_mapping.items():
                    value = row.get(field)
                    if value and value.strip():
                        value = value.strip()
                        start = text.find(value)
                        if start != -1:
                            end = start + len(value)
                            ents.append((start, end, label))

                ents = self.remove_overlapping_entities(ents)

                if ents:
                    train_data.append({"text": text, "entities": ents})
                    label_set.update([label for _, _, label in ents])

            return train_data, label_set

        except Exception as e:
            logging.error("Error loading training data", exc_info=True)
            raise CustomException(e)

    def train_and_save(self) -> NERTrainerArtifact:
        try:
            train_data, labels = self.load_data()

            for label in labels:
                self.ner.add_label(label)

            logging.info(f"Training on {len(train_data)} samples with {len(labels)} labels.")

            other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
            with self.nlp.disable_pipes(*other_pipes):
                optimizer = self.nlp.begin_training()
                for itn in range(self.config.num_iterations):
                    losses = {}
                    logging.info(f"📦 Iteration {itn + 1}")
                    for example in train_data:
                        doc = self.nlp.make_doc(example["text"])
                        ex = Example.from_dict(doc, {"entities": example["entities"]})
                        self.nlp.update([ex], drop=self.config.dropout, sgd=optimizer, losses=losses)
                    logging.info(f"Loss: {losses}")

            self.nlp.to_disk(self.config.output_model_dir)
            logging.info(f"✅ Model saved to: {self.config.output_model_dir}")

            return NERTrainerArtifact(
                model_path=self.config.output_model_dir,
                labels=list(labels),
                status="Success"
            )

        except Exception as e:
            logging.error("Training failed", exc_info=True)
            raise CustomException(e)
