import time
from pdf_reader import get_total_pages, read_articles_from_pdf
from weaviate_uploader import setup_weaviate, insert_articles

def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def main(pdf_file, batch_size_pdf=10):
    client = setup_weaviate()

    total_pages = get_total_pages(pdf_file)
    start_time = time.time()

    for pdf_batch_start in range(0, total_pages, batch_size_pdf):
        pdf_batch_end = min(pdf_batch_start + batch_size_pdf, total_pages)
        batch_start_time = time.time()

        print(f"Processing PDF pages {pdf_batch_start} to {pdf_batch_end - 1}")

        articles_batch = read_articles_from_pdf(pdf_file, pdf_batch_start, pdf_batch_end)
        insert_articles(client, articles_batch)

        batch_end_time = time.time()
        elapsed_batch = batch_end_time - batch_start_time
        elapsed_total = batch_end_time - start_time
        pages_done = pdf_batch_end
        pages_remaining = total_pages - pages_done
        estimated_remaining_time = (elapsed_total / pages_done) * pages_remaining

        print(colored(
            f"Batch took {format_time(elapsed_batch)}. Estimated remaining time: {format_time(estimated_remaining_time)}", "32"
        ))

    print("Inserting Articles complete")
    client.close()

if __name__ == "__main__":
    main("harrison.pdf", batch_size_pdf=10)
