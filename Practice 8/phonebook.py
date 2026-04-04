import csv,os,psycopg2
from connect import get_connection

FILE_PATH=r"C:\Users\acer\Documents\hefbvi\Practice 8\contacts.csv"

def create_table():
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS contacts(id SERIAL PRIMARY KEY,name TEXT NOT NULL,phone TEXT NOT NULL)")
        conn.commit()
        cur.close()
        conn.close()

def import_from_csv():
    if not os.path.exists(FILE_PATH):
        return
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        with open(FILE_PATH,"r",encoding="utf-8-sig") as f:
            reader=csv.reader(f)
            for row in reader:
                if row and len(row)>=2:
                    name,phone=row[0].strip(),row[1].strip()
                    cur.execute("SELECT 1 FROM contacts WHERE name=%s AND phone=%s",(name,phone))
                    if not cur.fetchone():
                        cur.execute("INSERT INTO contacts(name,phone) VALUES(%s,%s)",(name,phone))
        conn.commit()
        cur.close()
        conn.close()

def add_contact(name,phone):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("INSERT INTO contacts(name,phone) VALUES(%s,%s)",(name,phone))
        conn.commit()
        cur.close()
        conn.close()

def show_contacts():
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("SELECT name,phone FROM contacts")
        rows=cur.fetchall()
        for r in rows:
            print(r[0],r[1])
        cur.close()
        conn.close()

def run_sql_file(file):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        with open(file,"r") as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        conn.close()

def search_pattern(p):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s)",(p,))
        for r in cur.fetchall():
            print(r)
        cur.close()
        conn.close()

def pagination(l,o):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s,%s)",(l,o))
        for r in cur.fetchall():
            print(r)
        cur.close()
        conn.close()

def insert_or_update(n,p):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("CALL insert_or_update_user(%s,%s)",(n,p))
        conn.commit()
        cur.close()
        conn.close()

def insert_many():
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        names=["A","B","C"]
        phones=["123","abc","456"]
        cur.execute("CALL insert_many_users(%s,%s)",(names,phones))
        conn.commit()
        cur.close()
        conn.close()

def delete_value(v):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("CALL delete_contact(%s)",(v,))
        conn.commit()
        cur.close()
        conn.close()

if __name__=="__main__":
    create_table()
    import_from_csv()
    while True:
        print("1 Add")
        print("2 Show")
        print("3 Search")
        print("4 Pagination")
        print("5 InsertUpdate")
        print("6 InsertMany")
        print("7 Delete")
        print("8 RunFunctions")
        print("9 RunProcedures")
        print("0 Exit")
        c=input("> ")
        if c=="1":
            add_contact(input("Name: "),input("Phone: "))
        elif c=="2":
            show_contacts()
        elif c=="3":
            search_pattern(input("Pattern: "))
        elif c=="4":
            pagination(int(input("Limit: ")),int(input("Offset: ")))
        elif c=="5":
            insert_or_update(input("Name: "),input("Phone: "))
        elif c=="6":
            insert_many()
        elif c=="7":
            delete_value(input("Value: "))
        elif c=="8":
            run_sql_file("functions.sql")
        elif c=="9":
            run_sql_file("procedures.sql")
        elif c=="0":
            break
