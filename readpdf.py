import json
from pdfminer.high_level import extract_text

harrison_page1=41
no_of_pages=3
page_numbers = [harrison_page1 + i - 1 for i in range(1, no_of_pages)]  # Convert to zero-based indexing

# Extract all text in a single call
full_text = extract_text("harrison.pdf", page_numbers=page_numbers)

# Split text by form-feed ('\f'), which represents a new page in PDFs
texts_by_page = full_text.split("\f")  # pdfminer uses '\f' to separate pages

# Remove empty pages if any trailing empty strings exist
# texts_by_page = [page.strip() for page in texts_by_page if page.strip()]

dataset=[]
for i, text in enumerate(texts_by_page[:no_of_pages]):  # Show first 5 pages
    dataset.append({"page":f"{i+1}", "text":text})

data_string = json.dumps(dataset, indent=2)

# Write to a Python file
with open("dataset_file.py", "w") as f:
    f.write(f"dataset={data_string}\n")