from dotenv import load_dotenv
import os
import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

load_dotenv()

db_info = {
    "dbname" : os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "host": os.environ["DB_HOST"]
}

@contextmanager
def connect():
    conn = psycopg2.connect(**db_info, cursor_factory=RealDictCursor)
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    finally:
        conn.close()


def init_db():
    with connect() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS contacts(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        phone_number VARCHAR(15) NOT NULL,
        email VARCHAR(100) NOT NULL,
        favorite BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NULL,
        UNIQUE(first_name, last_name, phone_number)
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS contact_notes(
        id SERIAL PRIMARY KEY,
        note TEXT,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE)
        """)
    print("DB INITIALIZED......")
    print()


def drop_table():
    with connect() as cur:
        cur.execute("DROP TABLE IF EXISTS contact_notes CASCADE")
        cur.execute("DROP TABLE IF EXISTS contacts CASCADE")
    print("TABLES DROPPED......")
    print()


def add_contact(f_name,l_name,phone,email,note=None):
    sql = """INSERT INTO contacts(first_name,last_name,phone_number,email)
    VALUES (%s, %s, %s, %s) RETURNING id, first_name,last_name,phone_number"""
    try:
        with connect() as cur:
            cur.execute(sql,(f_name,l_name,phone,email))
            row = cur.fetchone()
            updated_row = cur.rowcount
            if updated_row > 0:
                print(f"Contact added: #{row['id']} - {row['first_name']} {row['last_name']} - {row['phone_number']}")
            else:
                print("Failed to add contact.")

            if note:
                sql_note = """INSERT INTO contact_notes(note,contact_id) VALUES (%s,%s)"""
                cur.execute(sql_note,(note,row['id']))
    except psycopg2.IntegrityError:
        print(f"Duplicate contact not added: [{f_name} {l_name}, {phone}]")
    except psycopg2.Error as e:
        print(f"Error occurred while adding contact: [{e}]")


def delete_contact(contact_id):
    try:
        sql = """DELETE FROM contacts WHERE id = %s RETURNING id, first_name, last_name,phone_number"""
        with connect() as cur:
            cur.execute(sql,(contact_id,))
            row = cur.fetchone()
            updated_row = cur.rowcount
            if updated_row > 0:
                print(f"Contact Deleted: #{row['id']} - {row['first_name']} {row['last_name']} - {row['phone_number']}")
            else:
                print("Failed to Delete contact.")
    except psycopg2.Error as e:
        print(f"Error occurred while adding contact: [{e}]")



def update_contact(contact_id,f_name=None,l_name=None,phone=None,email=None,note=None):
    sql = """UPDATE contacts SET"""
    params = []

    if f_name:
        sql += """ first_name = %s,"""
        params.append(f_name)

    if l_name:
        sql += """ last_name = %s,"""
        params.append(l_name)

    if phone:
        sql += """ phone_number = %s,"""
        params.append(phone)

    if email:
        sql += """ email = %s,"""
        params.append(email)

    params.append(contact_id)
    sql += """ updated_at = NOW() WHERE id = %s RETURNING id, first_name, last_name, phone_number"""

    try:
        with connect() as cur:
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            updated_row = cur.rowcount

            if updated_row > 0:
                print(f"Contact Updated: #{row['id']} - {row['first_name']} {row['last_name']} - {row['phone_number']}")
            else:
                print("Failed to Update contact.")

            if note:
                sql_note = """INSERT INTO contact_notes(note,contact_id) VALUES (%s,%s)"""
                cur.execute(sql_note,(note,contact_id))
    except psycopg2.IntegrityError:
        print(f"Duplicate contact not updated: [{f_name} {l_name}, {phone}]")

    except psycopg2.Error as e:
        print(f"Error occurred while updating contact: [{e}]")


def get_contacts():
    sql = """SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.phone_number, contacts.email, contact_notes.note, contacts.created_at, contacts.updated_at
    FROM contacts
    LEFT JOIN contact_notes
    ON contacts.id = contact_notes.contact_id ORDER BY contacts.first_name,contacts.last_name"""
    with connect() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("No contacts found.")

        print("ALL CONTACTS")
        print("="*40)
        for r in rows:
            print(f"""id : {r['id']}
    first_name : {r.get('first_name',None)}
    last_name : {r.get('last_name',None)}
    phone_number : {r.get('phone_number',None)}
    email : {r.get('email',None)}
    Note : {r.get('note',None)}
    created At : {r.get('created_at',None)}
    updated At : {r.get('updated_at',None)}
""")


def display():
    sql = """SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.phone_number
    FROM contacts
    LEFT JOIN contact_notes
    ON contacts.id = contact_notes.contact_id 
    ORDER BY contacts.id
    """

    with connect() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            print("Contacts List:")
            print("="*80)
            for r in rows:
                print(f"#id : {r['id']}",f"     |  @name : {r.get('first_name',None)} {r.get('last_name',None)}",f"     |  @phone_number : {r.get('phone_number',None)}",sep="\t")
                print("="*80)
            return True
        else:
            print("No contacts found.")
            return False


def favorite(contact_id):
    sql = """UPDATE contacts
    SET favorite = TRUE where id = %s AND favorite = FALSE RETURNING id, first_name, last_name, phone_number"""

    with connect() as cur:
        cur.execute(sql,(contact_id,))
        row = cur.fetchone()
        updated_row = cur.rowcount
        if updated_row > 0:
            print(f"Contact Favorited: #{row['id']} - {row['first_name']} {row['last_name']} - {row['phone_number']}")
        else:
            print("Failed to Favorite contact.")


def unfavorite(contact_id):
    sql = """UPDATE contacts
    SET favorite = FALSE where id = %s AND favorite = TRUE RETURNING id, first_name, last_name, phone_number"""

    with connect() as cur:
        cur.execute(sql,(contact_id,))
        row = cur.fetchone()
        updated_row = cur.rowcount
        if updated_row > 0:
            print(f"Contact Unfavorited: #{row['id']} - {row['first_name']} {row['last_name']} - {row['phone_number']}")
        else:
            print("Failed to Unfavorite contact.")

 
def filter(id=None,name=None,phone=None,email=None,favorite=False):
    sql = """SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.phone_number, contacts.email, contact_notes.note, contacts.created_at, contacts.updated_at
    FROM contacts
    LEFT JOIN contact_notes
    ON contacts.id = contact_notes.contact_id """

    params = []
    header = ""

    if id:
        sql += """WHERE contacts.id = %s"""
        params.append(id)
        header = f"Filtering by ID: {id}"

    elif name:
        sql += """WHERE contacts.first_name ILIKE %s OR contacts.last_name ILIKE %s"""
        params.append(f"%{name}%")
        params.append(f"%{name}%")
        header = f"Filtering by Name: {name}"

    elif phone:
        sql += """WHERE contacts.phone_number ILIKE %s"""
        params.append(f"%{phone}%")
        header = f"Filtering by Phone Number: {phone}"

    elif email:
        sql += """WHERE contacts.email ILIKE %s"""
        params.append(f"%{email}%")
        header = f"Filtering by Email: {email}"

    elif favorite:
        sql += """WHERE contacts.favorite = TRUE"""
        params = None
        header = f"Filtering by Favorite: {favorite}"

    
    with connect() as cur:
        cur.execute(sql,tuple(params)) if params else cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            print("No matching contacts found.")
            return
        print(header)
        print("="*80)
        for r in rows:
            print(f"""id : {r['id']}
    first_name : {r.get('first_name',None)}
    last_name : {r.get('last_name',None)}
    phone_number : {r.get('phone_number',None)}
    email : {r.get('email',None)}
    Note : {r.get('note',None)}
    created At : {r.get('created_at',None)}
    updated At : {r.get('updated_at',None)}""")

def stats():
    sql = """SELECT COUNT(*) AS contact_count,
    COUNT(
    CASE
    WHEN favorite = TRUE THEN 1
    END) AS favorite_count,
    COUNT(
    CASE
    WHEN favorite = FALSE THEN 1
    END) AS non_favorite_count,
    COUNT(updated_at) AS updates
    FROM contacts
    """
    with connect() as cur:
        cur.execute(sql)
        row = cur.fetchone()
        print("Contact Statistics:")
        print("="*80)
        print(f"Total contacts: {row['contact_count']}")
        print(f"Favorite contacts: {row['favorite_count']}")
        print(f"Non-favorite contacts: {row['non_favorite_count']}")
        print(f"Total Updates : {row['updates']}")
        print("="*80)
        print()

if __name__ == "__main__":
    init_db()
    #add_contact("Amon","Blasphemus","1234567890","amon.blasphemus@example.com","A good friend")
    #display()
    #update_contact(2,"Yamael","phemus","0987654321","samael.phemus@example.com")
    get_contacts()
    #drop_table()
    stats()
    #filter(name="phemus")