from pdfminer.high_level import extract_text

text = extract_text(pdf_file="harrison.pdf", page_numbers=[82])

print("Here's the text from page 80 of the PDF:\n\n")
print(text)