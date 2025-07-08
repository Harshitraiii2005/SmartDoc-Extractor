import spacy
import json
from spacy.training import offsets_to_biluo_tags, Example

INPUT_JSON = "extracted_fields_summary.json"
OUTPUT_JSON = "ner_training_data_clean.json"

# Load spaCy blank model
nlp = spacy.blank("en")

# Read the extracted data
with open(INPUT_JSON, encoding="utf-8") as f:
    data = json.load(f)

clean_data = []
misaligned = 0
conflicting = 0
total = len(data)

print(f"\n🔍 Validating {total} extracted examples...\n")

for i, item in enumerate(data):
    text = item.get("Text", "")
    doc = nlp.make_doc(text)

    # Construct entities list from fields
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
        # Check alignment
        tags = offsets_to_biluo_tags(doc, entities)
        if "-" in tags:
            print(f"⚠️ Misaligned entity in example {i}")
            misaligned += 1
            continue

        # Check for conflicting spans
        Example.from_dict(doc, {"entities": entities})

        # If passes all checks
        clean_data.append((text, {"entities": entities}))

    except ValueError as e:
        print(f"❌ Error in example {i}: {e}")
        conflicting += 1

# Save clean examples
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, indent=2, ensure_ascii=False)

print("\n📊 Validation Summary:")
print(f"✅ Total: {total}")
print(f"🧼 Clean: {len(clean_data)}")
print(f"⚠️ Misaligned: {misaligned}")
print(f"❌ Conflicting: {conflicting}")
print(f"\n✅ Saved {len(clean_data)} valid examples to '{OUTPUT_JSON}'")
