import os
import json
from extract_fields import extract_fields

input_dir = "cleaned_texts"
output_json = "extracted_fields_summary.json"

# Collect all extracted data
all_data = []

# Process each cleaned text file
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        fields = extract_fields(text)
        fields["Filename"] = filename  # Track which file this came from
        fields["Text"] = text          # Optional: Include raw text too (for debugging/training)
        all_data.append(fields)

        print(f"\n✅ Extracted fields from: {filename}")
        for k, v in fields.items():
            print(f"  {k}: {v}")

# Save all data as JSON
if all_data:
    with open(output_json, "w", encoding="utf-8") as jsonfile:
        json.dump(all_data, jsonfile, indent=2, ensure_ascii=False)

    print(f"\n✅ All results saved to: {output_json}")
else:
    print("\n⚠️ No files found or no data extracted.")
