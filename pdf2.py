import os
import re
import fitz  # PyMuPDF library for PDF text extraction
import pandas as pd

def save_text_to_file(text, output_dir, filename):
    """
    Save the extracted text to a separate file.
    :param text: The text content extracted from the PDF.
    :param output_dir: Directory to save text files.
    :param filename: Name of the original PDF file.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the text file name based on the PDF file name
    text_file_name = os.path.splitext(filename)[0] + ".txt"
    text_file_path = os.path.join(output_dir, text_file_name)

    # Save the text to the file
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)

def extract_name_from_text(text):
    """
    Extract the full name from the given Persian text.
    Assumes the name appears after a keyword like 'به نام'.
    """
    # Define a regex pattern to match names (e.g., appears after 'گواهی').
    # name_pattern = r"گواهی\s+([\u0600-\u06FF\s]+)"  # Persian name regex
    # match = re.search(name_pattern, text)
    text = clear_text(text)
    start_pos = max(text.find("ﺟﻨﺎﺏ"), text.find("ﺳﺮﮐﺎﺭ"))
    end_pos = text.find("ﺁﻣﻮﺯﺵ ﮐﺎﺭﺷﻨﺎﺳﺎﻥ ﺍﺗﻮﻣﺎﺳﯿﻮﻥ ﺍﺩﺍﺭﯼ")
    match = text[start_pos : end_pos]
    print(start_pos, end_pos, match)
    if match:
        return match
    else:
        return False

def clear_text(text):
    cleared_text = ""
    cleared_text = ''.join(c for c in text if c.isalpha() or c == ' ')
    return cleared_text
    
def process_pdf_directory(input_dir, text_output_dir, output_csv):
    """
    Process all PDF files in the input directory, save extracted text to separate files,
    extract names, and save results to a CSV file.
    """
    # Store extracted information
    results = []

    # Loop through all PDF files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            try:
                # Open the PDF file and extract text
                pdf_document = fitz.open(file_path)
                text = ""
                for page in pdf_document:
                    text += page.get_text()
                pdf_document.close()

                # Save extracted text to a separate file
                save_text_to_file(text, text_output_dir, filename)

                # Extract the name from text
                full_name = extract_name_from_text(text)

                if full_name:
                    results.append({
                        "PDF File": filename,
                        "Certificate Owner": full_name
                    })
                else:
                    results.append({
                        "PDF File": filename,
                        "Certificate Owner": "Name Not Found"
                    })
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Convert results to a DataFrame and save as CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Results saved to {output_csv}")

# Directories and file paths
input_directory = "./certificates"  # Directory containing PDF files
text_output_directory = "./certificates/texts"  # Directory for extracted text files
output_csv_file = "./certificates/output_certificates.csv"  # Path for the final CSV file

# Run the script
process_pdf_directory(input_directory, text_output_directory, output_csv_file)
