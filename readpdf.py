import json
import os
import argparse
from pdfminer.high_level import extract_text

# Default values
harrison_page1 = 41
no_of_pages = 20
start_at_page = 947

# Parse command line arguments
parser = argparse.ArgumentParser(description="Extract text from PDF pages.")
parser.add_argument('--pages', type=int, default=no_of_pages, help='Number of pages to extract')
parser.add_argument('--start', type=int, default=start_at_page, help='Starting page number')
args = parser.parse_args()

# Use the values from command line arguments or defaults
print(f"Extracting {args.pages} pages starting from page {args.start}")
no_of_pages = args.pages
start_at_page = args.start

page_numbers = [harrison_page1 + i - 1 for i in range(start_at_page, start_at_page + no_of_pages)]  # Convert to zero-based indexing

# Extract all text in a single call
full_text = extract_text("harrison.pdf", page_numbers=page_numbers)

# Split text by form-feed ('\f'), which represents a new page in PDFs
texts_by_page = full_text.split("\f")  # pdfminer uses '\f' to separate pages

dataset = []
output_dir = "output_pages"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for i, text in enumerate(texts_by_page[:no_of_pages]):  # Show first 5 pages
    page_data = {"page": f"{i + start_at_page}", "text": text}
    dataset.append(page_data)
    
    # Write each page to an individual JSON file
    page_file_path = os.path.join(output_dir, f"page_{i + start_at_page}.json")
    with open(page_file_path, "w") as page_file:
        json.dump(page_data, page_file, indent=2)

data_string = json.dumps(dataset, indent=2)

# Write to a Python file
with open("dataset_file.py", "w") as f:
    f.write(f"dataset={data_string}\n")