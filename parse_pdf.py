import fitz  # PyMuPDF
import sqlite3

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

text = parse_pdf("/mnt/data/阑尾炎资料.pdf")

conn = sqlite3.connect('text_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS documents (content TEXT)''')
cursor.execute("INSERT INTO documents (content) VALUES (?)", (text,))
conn.commit()
conn.close()
