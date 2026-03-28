import csv
import os
import psycopg2
from connect import get_connection

# Твой путь к файлу
FILE_PATH = r"C:\Users\acer\Documents\hefbvi\Practice 7\contacts.csv"

def create_table():
    conn = get_connection()
    if conn:
        curr = conn.cursor()
        curr.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        conn.commit()
        curr.close()
        conn.close()

def import_from_csv():
    if not os.path.exists(FILE_PATH):
        print(f"Файл не найден по пути: {FILE_PATH}")
        return
    
    conn = get_connection()
    if conn:
        curr = conn.cursor()
        with open(FILE_PATH, mode='r', encoding='utf-8-sig') as f:
            # Если в файле точки с запятой, замени delimiter=',' на delimiter=';'
            reader = csv.reader(f, delimiter=',') 
            for row in reader:
                if row and len(row) >= 2:
                    name, phone = row[0].strip(), row[1].strip()
                    curr.execute("SELECT id FROM contacts WHERE name = %s AND phone = %s", (name, phone))
                    if not curr.fetchone():
                        curr.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        curr.close()
        conn.close()

def add_contact(name, phone):
    conn = get_connection()
    if conn:
        curr = conn.cursor()
        curr.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        curr.close()
        conn.close()
        print("Done!")

def show_contacts():
    conn = get_connection()
    if conn:
        curr = conn.cursor()
        curr.execute("SELECT name, phone FROM contacts")
        rows = curr.fetchall()
        if not rows:
            print("Empty")
        else:
            for row in rows:
                print(f"{row[0]}: {row[1]}")
        curr.close()
        conn.close()

if __name__ == "__main__":
    create_table()
    import_from_csv()
    while True:
        print("\n1. Add\n2. Show\n3. Exit")
        choice = input("> ")
        if choice == "1":
            add_contact(input("Name: "), input("Phone: "))
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            break