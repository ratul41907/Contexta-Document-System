import sqlite3

def view_data():
    conn = sqlite3.connect('E:/Construction_AI_Project/extracted_data.db')  # Path to DB

    cursor = conn.cursor()

    # Fetch all rows from the 'extracted_text' table
    cursor.execute('SELECT * FROM extracted_text')
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Filename: {row[1]}")
        print(f"Page Number: {row[2]}")
        print(f"Text Content: {row[3]}")
        print(f"Extraction Date: {row[4]}")
        print(f"Status: {row[5]}")
        print("\n---\n")

    conn.close()

# Run the function to view the database content
view_data()
