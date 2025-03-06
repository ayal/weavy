import subprocess
import os
import json
import time

start_at_page = 50

def format_time(seconds):
    if seconds >= 3600:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f'{hours}h {minutes}m {seconds}s'
    elif seconds >= 60:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f'{minutes}m {seconds}s'
    else:
        return f'{int(seconds)}s'

def extract_text_from_pdf(pdf_path, output_dir, progress_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the number of pages in the PDF
    result = subprocess.run(['pdfinfo', pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='latin1')
    for line in result.stdout.splitlines():
        if line.startswith('Pages:'):
            num_pages = int(line.split(':')[1].strip())
            break
    
    # Determine the starting page
    if start_at_page > 0:
        last_processed_page = start_at_page - 1
    elif os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            last_processed_page = int(f.read().strip())
    else:
        last_processed_page = 0
    
    total_time = 0
    # Extract text from each page starting from the last processed page + 1
    for page in range(last_processed_page + 1, num_pages + 1):
        start_time = time.time()
        
        output_file = os.path.join(output_dir, f'page_{page}.json')
        result = subprocess.run(['pdftotext', '-layout', '-f', str(page), '-l', str(page), pdf_path, '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='latin1')
        text = result.stdout
        data = {
            'text': text,
            'page': page
        }
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        
        percentage = (page / num_pages) * 100
        print(f'Extracted text from page {page}/{num_pages} ({percentage:.2f}%) to {output_file}')
        
        # Update the progress file
        with open(progress_file, 'w') as f:
            f.write(str(page))
        
        if page % 5 == 0:  # Estimate time after every 5 pages
            avg_time_per_page = total_time / page
            remaining_pages = num_pages - page
            estimated_time_remaining = avg_time_per_page * remaining_pages
            formatted_time = format_time(estimated_time_remaining)
            print(f'Estimated time remaining: {formatted_time}')

if __name__ == '__main__':
    pdf_path = 'harrison.pdf'
    output_dir = 'output_pages'
    progress_file = 'xpdf-progress.txt'
    extract_text_from_pdf(pdf_path, output_dir, progress_file)