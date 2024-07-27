import os

import requests
from tqdm import tqdm

# Define the folder containing the PDF files and the API endpoint
folder_path = 'pdfs'
api_endpoint = 'http://localhost:8000/files/upload?chunk_size=200'

# Get a list of all PDF files in the folder
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Upload each PDF file with a progress bar
for pdf_file in tqdm(pdf_files, desc="Uploading PDF files", unit="file"):
    file_path = os.path.join(folder_path, pdf_file)

    with open(file_path, 'rb') as f:
        files = {'file': (pdf_file, f, 'application/pdf')}
        headers = {'accept': 'application/json'}
        response = requests.post(api_endpoint, headers=headers, files=files)

        if response.status_code == 200:
            tqdm.write(f"Successfully uploaded: {pdf_file}")
        else:
            tqdm.write(f"Failed to upload: {pdf_file}, Status Code: {response.status_code}")

print("All files have been processed.")
