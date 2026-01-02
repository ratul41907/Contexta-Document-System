import sqlite3
import os

# Create and initialize the database
def create_database():
    # Define the path to the database file
    db_path = 'E:/Construction_AI_Project/extracted_data.db'  # Path to where the DB will be stored

    # Connecting to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the existing table (if it exists)
    cursor.execute('DROP TABLE IF EXISTS extracted_text')

    # Create a new table to store extracted text content
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            page_number INTEGER,
            text_content TEXT,
            extraction_date TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Insert extracted text into the database
def insert_extracted_text(filename, page_number, text_content, extraction_date, status):
    db_path = 'E:/Construction_AI_Project/extracted_data.db'  # Path to where the DB is stored

    # Connecting to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the text into the table
    cursor.execute('''
        INSERT INTO extracted_text (filename, page_number, text_content, extraction_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, page_number, text_content, extraction_date, status))

    conn.commit()
    conn.close()

# Check the content of the database (retrieve all rows)
def display_database_content():
    db_path = 'E:/Construction_AI_Project/extracted_data.db'  # Path to where the DB is stored

    # Connecting to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to retrieve all rows from the 'extracted_text' table
    cursor.execute('SELECT * FROM extracted_text')
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Filename: {row[1]}")
        print(f"Page Number: {row[2]}")
        print(f"Text Content: {row[3]}")
        print(f"Extraction Date: {row[4]}")
        print(f"Status: {row[5]}")
        print("\n---\n")

    conn.close()

# Main execution block for testing
if __name__ == "__main__":
    create_database()  # Create the database and table
    
    # Insert sample text into the database
    insert_extracted_text("sample_pdf.pdf", 1, "This is the text extracted from the first page.", "2023-10-11 12:00:00", "success")
    insert_extracted_text("sample_pdf.pdf", 2, "This is the text extracted from the second page.", "2023-10-11 12:10:00", "success")
    
    display_database_content()  # Display content to check if it was inserted correctly
