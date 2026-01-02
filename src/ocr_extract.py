import os
import re
import PyPDF2
from PIL import Image
import pytesseract

# Clean up the extracted text
def clean_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove unwanted extra spaces around sentences
    text = text.strip()
    return text

# Function to extract text from the PDF and print it
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()  # Extract text from the page
            cleaned_text = clean_text(text)
            
            print(f"Text from page {page_number + 1}:")
            print(cleaned_text)
            print("\n---\n")

# Function to extract text from PDF and save it to a specific file path
def save_text_to_file(pdf_path, output_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the output file with UTF-8 encoding to handle special characters
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                text = page.extract_text()  # Extract text from the page
                cleaned_text = clean_text(text)
                
                output_file.write(f"Text from page {page_number + 1}:\n")
                output_file.write(cleaned_text)
                output_file.write("\n---\n")

# Function to extract text from an image and print it
def extract_text_from_image(image_path):
    if os.path.exists(image_path):  # Check if file exists
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        cleaned_text = clean_text(text)
        
        print(f"Text extracted from image {image_path}:")
        print(cleaned_text)
        print("\n---\n")
    else:
        print(f"Error: The file at {image_path} does not exist.")

# Function to save extracted text from image to a file
def save_image_text_to_file(image_path, output_path):
    if os.path.exists(image_path):  # Check if file exists
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        cleaned_text = clean_text(text)
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open the output file with UTF-8 encoding to handle special characters
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("Text extracted from image:\n")
            output_file.write(cleaned_text)
            output_file.write("\n---\n")
    else:
        print(f"Error: The file at {image_path} does not exist.")

# Main execution block
if __name__ == "__main__":
    # For PDF extraction
    pdf_file_path = 'E:/Construction_AI_Project/data/plan.pdf'  # Update with your PDF file path
    extract_text_from_pdf(pdf_file_path)

    output_file_path_pdf = 'E:/Construction_AI_Project/data/extracted_text_from_pdf.txt'  # Update the output path if needed
    save_text_to_file(pdf_file_path, output_file_path_pdf)  # Save to the custom path

    # For image extraction
    image_file_path = 'E:/Construction_AI_Project/data/sample_image.png'  # Update with your image file path
    extract_text_from_image(image_file_path)

    output_file_path_image = 'E:/Construction_AI_Project/data/extracted_text_from_image.txt'  # Update the output path if needed
    save_image_text_to_file(image_file_path, output_file_path_image)  # Save to the custom path
