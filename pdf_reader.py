from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage

def get_total_pages(pdf_file):
    with open(pdf_file, "rb") as file:
        return len(list(PDFPage.get_pages(file)))

def read_articles_from_pdf(pdf_file, start_page, end_page):
    articles = []
    for page_number in range(start_page, end_page):
        print(f"Reading page {page_number}")
        page_text = extract_text(pdf_file, page_numbers=[page_number])
        lines = page_text.strip().split('\n')
        title = lines[0] if lines else f"Page {page_number}"
        content = '\n'.join(lines[1:]) if len(lines) > 1 else "No content"
        url = f"https://my-harrison.com?page={page_number}"
        articles.append({
            "title": title,
            "content": content,
            "url": url
        })
    return articles
