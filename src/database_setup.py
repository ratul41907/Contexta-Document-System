import sqlite3
import os

# Create and initialize the database
def create_database():
    # Define the path to the database file
    db_path = 'E:/Construction_AI_Project/extracted_data.db'  # Path to where the DB will be stored

    # Check if the database file exists; if not, create it
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create a table to store extracted text content
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
        print("Database and table created successfully.")
    else:
        print("Database already exists.")

# Main execution block for testing
if __name__ == "__main__":
    create_database()  # Create the database and table
