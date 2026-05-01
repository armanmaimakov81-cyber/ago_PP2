import json,os
from connect import get_connection

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

def run_sql(file):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        with open(os.path.join(BASE_DIR,file),"r",encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        conn.close()

def add_contact(name,email,birthday):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute(
            "INSERT INTO contacts(name,email,birthday) VALUES(%s,%s,%s)",
            (name,email,birthday)
        )
        conn.commit()
        cur.close()
        conn.close()

def add_phone(name,phone,type_):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("SELECT id FROM contacts WHERE name ILIKE %s",(name,))
        cid=cur.fetchone()
        if cid:
            cur.execute(
                "INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",
                (cid[0],phone,type_)
            )
            conn.commit()
        cur.close()
        conn.close()

def move_group(name,group_id):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute(
            "UPDATE contacts SET group_id=%s WHERE name ILIKE %s",
            (group_id,name)
        )
        conn.commit()
        cur.close()
        conn.close()

def search(q):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s)",(q,))
        for r in cur.fetchall():
            print(r)
        cur.close()
        conn.close()

def filter_group(group_id):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("""
        SELECT c.name,c.email,c.birthday,c.group_id
        FROM contacts c
        WHERE c.group_id=%s
        """,(group_id,))
        for r in cur.fetchall():
            print(f"NAME: {r[0]} | EMAIL: {r[1]} | BIRTHDAY: {r[2]} | GROUP_ID: {r[3]}")
        cur.close()
        conn.close()

def sort_by(field):
    conn=get_connection()
    if conn:
        cur=conn.cursor()

        allowed=["name","birthday","created_at"]
        if field not in allowed:
            print("invalid field")
            return

        cur.execute(f"SELECT name,email FROM contacts ORDER BY {field}")
        for r in cur.fetchall():
            print(r)

        cur.close()
        conn.close()

def export_json():
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute("""
        SELECT c.name,c.email,c.birthday,c.group_id,p.phone,p.type
        FROM contacts c
        LEFT JOIN phones p ON c.id=p.contact_id
        """)
        data=[]
        for r in cur.fetchall():
            data.append({
                "name":r[0],
                "email":r[1],
                "birthday":str(r[2]),
                "group_id":r[3],
                "phone":r[4],
                "type":r[5]
            })
        with open("contacts.json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
        cur.close()
        conn.close()

def import_json():
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        with open("contacts.json","r",encoding="utf-8") as f:
            data=json.load(f)

        for d in data:
            cur.execute("SELECT id FROM contacts WHERE name=%s",(d["name"],))
            if cur.fetchone():
                continue

            cur.execute(
                "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s)",
                (d["name"],d["email"],d["birthday"],d["group_id"])
            )

        conn.commit()
        cur.close()
        conn.close()

def paginate(limit,offset):
    conn=get_connection()
    if conn:
        cur=conn.cursor()
        cur.execute(
            "SELECT name,email,group_id FROM contacts LIMIT %s OFFSET %s",
            (limit,offset)
        )
        for r in cur.fetchall():
            print(f"{r[0]} | {r[1]} | group_id={r[2]}")
        cur.close()
        conn.close()


if __name__=="__main__":
    while True:
        print("\n1 schema")
        print("2 procedures")
        print("3 add contact")
        print("4 add phone")
        print("5 move group")
        print("6 search")
        print("7 filter group")
        print("8 sort")
        print("9 export")
        print("10 import")
        print("11 paginate")
        print("0 exit")

        c=input("> ")

        if c=="1":
            run_sql(r"C:\Users\acer\Documents\hefbvi\TSIS 1\schema.sql")
        elif c=="2":
            run_sql(r"C:\Users\acer\Documents\hefbvi\TSIS 1\procedures.sql")
        elif c=="3":
            add_contact(input("name "),input("email "),input("birthday "))
        elif c=="4":
            add_phone(input("name "),input("phone "),input("type "))
        elif c=="5":
            move_group(input("name "),input("group id "))
        elif c=="6":
            search(input("query "))
        elif c=="7":
            filter_group(input("group id "))
        elif c=="8":
            sort_by(input("name/birthday/created_at "))
        elif c=="9":
            export_json()
        elif c=="10":
            import_json()
        elif c=="11":
            paginate(int(input("limit ")),int(input("offset ")))
        elif c=="0":
            break
