import os
import re
import sqlite3
import pytesseract
from PIL import Image
import PyPDF2

# Clean up the extracted text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove extra spaces around sentences
    return text

# Function to extract text from the PDF and store it in the database
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()  # Extract text from the page
            cleaned_text = clean_text(text)

            # Store the extracted text in the database
            insert_extracted_text(pdf_path, page_number + 1, cleaned_text)

# Function to extract text from the image and store it in the database
def extract_text_from_image(image_path):
    if os.path.exists(image_path):  # Check if file exists
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        cleaned_text = clean_text(text)

        # Store the extracted text in the database
        insert_extracted_text(image_path, 1, cleaned_text)

# Function to insert the extracted text into the database
def insert_extracted_text(filename, page_number, text_content):
    db_path = 'E:/Construction_AI_Project/extracted_data.db'  # Set the path to where the DB is stored

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the extracted text into the table
    cursor.execute(''' 
        INSERT INTO extracted_text (filename, page_number, text_content, extraction_date, status)
        VALUES (?, ?, ?, datetime('now'), ?)
    ''', (filename, page_number, text_content, 'success'))  # Adding current date as extraction date

    conn.commit()
    conn.close()

# Function to process all PDF and image files in the 'data' folder
def process_files():
    data_folder = 'E:/Construction_AI_Project/data'  # Path to your 'data' folder

    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)

        if file_name.endswith(".pdf"):
            extract_text_from_pdf(file_path)  # Extract from PDF
        elif file_name.endswith((".png", ".jpg", ".jpeg")):  # Add image file formats you want to process
            extract_text_from_image(file_path)  # Extract from image

# Main function to run the extraction process
if __name__ == "__main__":
    process_files()  # Start the text extraction process for all files in 'data' folder
