from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from .expense_categories import EXPENSE_CATEGORIES,categories

load_dotenv()

db_info = {
    "dbname" : os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "host": os.environ["DB_HOST"]
}


@contextmanager
def connect():
    conn = psycopg2.connect(**db_info,cursor_factory=RealDictCursor)
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    finally:
        conn.close()


def init_db():
    try:
        with connect() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            category VARCHAR(100) UNIQUE NOT NULL
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
            id SERIAL PRIMARY KEY,
            amount NUMERIC(10,2) NOT NULL DEFAULT 0.0,
            description TEXT NOT NULL,
            category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
            date DATE NOT NULL DEFAULT CURRENT_DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())
            """)

            c = categories
            for i in c:
                cur.execute("""INSERT INTO categories(category)
                VALUES(%s) RETURNING *""",(i,))

                row = cur.fetchone()
                if row:
                    print(f"Added Category : #{row["id"]} - {row["category"]}")
         
    except psycopg2.IntegrityError as e:
        pass
    except psycopg2.Error as e:
        print(f"An Error Occured : [{e}]")

    print("DB INITIALIZED......")
    print()


def drop_table():
    with connect() as cur:
        cur.execute("DROP TABLE IF EXISTS expenses CASCADE")
        cur.execute("DROP TABLE IF EXISTS categories CASCADE")
    print("TABLES DROPPED......")
    print()

def category_suggestions(description):
    categ = []
    for key,values in EXPENSE_CATEGORIES.items():
        for value in values:
            if value.lower() in description.lower() or key.lower() in description.lower():
                categ.append(key)
    if not categ:
        categ = ["General"]

    return set(categ)

def add_expense(amount,description):
    index_category = {}
    c = category_suggestions(description)
    
    print("CHOOSE CATEGORIES")
    print("="*30)
    for index,categ in enumerate(c,start=1):
        print([index],categ)
    print([len(c)+1],"Category Not Listed, ADD CATEGORY...")

    print()
    opt = input("   Option IN : ")
    print()

    for index,categ in enumerate(c,start=1):
        index_category[index] = categ
        index_category[len(c)+1] = "Category Not Listed, ADD CATEGORY..."

    index_category = dict(sorted(index_category.items()))
    f = False
    for index,category in index_category.items():
        if opt == str(index):
            try:
                with connect() as cur:
                    cur.execute("""SELECT * FROM categories""")
                    rows = cur.fetchall()
                    for row in rows:
                        if category == row["category"]:
                            cur.execute("""INSERT INTO expenses(amount,description,category_id)
                            VALUES(%s,%s,%s) RETURNING id,amount""",(amount,description,row["id"]))
                            row = cur.fetchone()
                            updated_rows = cur.rowcount
                            
                            if updated_rows > 0:
                                print(f"Expense Added : #{row["id"]} - {row["amount"]}")
                            else:
                                print("Failed to add Expense...")
                            f = True

            except psycopg2.Error as e:
                print(f"Error occurred while adding contact: [{e}]")
            break
        
        elif opt == str(len(c)+1):
            input_c = input("ADD CATEGORY : ")
            print()
            try:
                with connect() as cur:
                    cur.execute("""INSERT INTO categories(category)
                    VALUES(%s) RETURNING *""",(input_c,))
                    row = cur.fetchone()
                    cur.execute("""INSERT INTO expenses(amount,description,category_id)
                    VALUES(%s,%s,%s) RETURNING id,amount""",(amount,description,row["id"]))
                    row0 = cur.fetchone()
                    updated_rows = cur.rowcount
                    
                    if updated_rows > 0:
                        print(f"Added Category : #{row["id"]} - {row["category"]}")
                        print(f"Expense Added : #{row0["id"]} - {row0["amount"]}")
                    else:
                        print("Failed to add Expense...")
                    f = True
            except psycopg2.Error as e:
                print(f"Error occurred while adding contact: [{e}]")
            break

    if not f:
        print("Invalid Option...")
        

def display_expense():
    sql = """SELECT expenses.id,expenses.amount,categories.category,expenses.created_at
    FROM expenses
    LEFT JOIN categories
    ON categories.id = expenses.category_id"""

    with connect() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            print("Expense List:")
            print("="*90)
            for row in rows:
                print(f"@#id : {row["id"]}",f"** @amount : ${row["amount"]}",f"** @category : {row["category"]}",f"** @created_at : {row["created_at"]}",sep="\t")
                print("="*90)
            return True
        else:
            print("No expenses Found ....")
            return False

def get_expenses():
    sql = """SELECT expenses.id,expenses.amount,expenses.description,categories.category,expenses.created_at
    FROM expenses
    LEFT JOIN categories
    ON categories.id = expenses.category_id"""


    with connect() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

        if not rows:
            print("No Expenses Found...")

        print("ALL EXPENSES:")
        print("="*80)
        for row in rows:
            print(f"""id : {row["id"]}
    amount : {row["amount"]}
    description : {row["description"]}
    category : {row["category"]}
    created_at : {row["created_at"]}
""")
            

def delete_expense(expense_id):
    sql = """DELETE FROM expenses WHERE id = %s RETURNING id,amount,category_id"""
    try:
        with connect() as cur:
            cur.execute(sql,(expense_id,))
            row = cur.fetchone()
            updated_row = cur.rowcount

            if updated_row > 0:
                print(f"Deleted expense : #{row["id"]} - ${row["amount"]} - #{row["category_id"]}")

            else:
                print("Failed to Delete expense...")
    except psycopg2.Error as e:
        print(f"Error occurred while adding contact: [{e}]")
                                                                                            

def update_expense(expense_id,amount=None,description=None):
    sql = """UPDATE expenses SET"""
    params = []
    index_category = {}
    

    if amount:
        sql += """ amount = %s"""
        params.append(amount)

    if description:
        if amount:
            sql += """, description = %s"""
        else:
            sql += """ description = %s"""
        params.append(description)

        c = category_suggestions(description)
        print("CHOOSE CATEGORIES")
        print("="*30)
        for index,categ in enumerate(c,start=1):
            print([index],categ)
        print([len(c)+1],"Category Not Listed, ADD CATEGORY...")

        print()
        opt = input("   Option IN : ")
        print()
        
        for index,categ in enumerate(c,start=1):
            index_category[index] = categ
            index_category[len(c)+1] = "Category Not Listed, ADD CATEGORY..."
        
    index_category = dict(sorted(index_category.items()))

    f = False
    for index,category in index_category.items():
        if opt == str(index):
            try:
                with connect() as cur:
                    cur.execute("""SELECT * FROM categories""")
                    rows = cur.fetchall()
                    for row in rows:
                        if category == row["category"]:
                            cur.execute("""UPDATE expenses SET category_id = %s WHERE id = %s RETURNING id""",(row["id"],expense_id))
                            row = cur.fetchone()
                            updated_rows = cur.rowcount
                            
                            if updated_rows > 0:
                                print(f"Updated Category : #{row["id"]}")
                            else:
                                print("Failed to update category : [INVALID ID] / [INVALID INPUT]")
                            f = True


            except psycopg2.Error as e:
                print(f"Error occurred while adding contact: [{e}]")
            break

        elif opt == str(len(c)+1):
            input_c = input("ADD CATEGORY : ")
            print()
            try:
                with connect() as cur:
                    cur.execute("""INSERT INTO categories(category)
                    VALUES(%s) RETURNING *""",(input_c,))
                    row = cur.fetchone()
                    cur.execute("""UPDATE expenses SET category_id = %s WHERE id = %s RETURNING id""",(row["id"],expense_id))
                    row0 = cur.fetchone()
                    updated_rows = cur.rowcount
                    
                    if updated_rows > 0:
                        print(f"Added Category : #{row["id"]} - {row["category"]}")
                        print(f"Updated Category : #{row["id"]}")
                    else:
                        print("Failed to update category : [INVALID ID] / [INVALID INPUT]...")
                    f = True

            except psycopg2.Error as e:
                print(f"Error occurred while adding contact: [{e}]")
            break

    if not f:
        print("INVALID Category OPTION....")

    sql += """ WHERE id = %s RETURNING id,amount,category_id"""
    params.append(expense_id)


    try:
        with connect() as cur:
            cur.execute(sql,tuple(params))
            row = cur.fetchone()
            updated_row = cur.rowcount

            if updated_row > 0:
                print(f"UPDATED expense : #{row["id"]} - ${row["amount"]} - #{row["category_id"]}")
            else:
                print("Failed to Update expense")
    except psycopg2.Error as e:
        print(f"An error ocuured WHILE updating expense : [{e}]")


def load_expense(expense_id):
    sql = """SELECT expenses.id,expenses.amount,expenses.description,categories.category,expenses.created_at
        FROM expenses
        LEFT JOIN categories
        ON categories.id = expenses.category_id
        WHERE expenses.id = %s"""
    
    
    with connect() as cur:
        cur.execute(sql,(expense_id,))
        row = cur.fetchone()

        if row:
            print("LOADED EXPENSE:")
            print("="*80)
            
            print(f"""id : {row["id"]}
        amount : {row["amount"]}
        description : {row["description"]}
        category : {row["category"]}
        created_at : {row["created_at"]}
    """)

        else:
            print("No Expenses Found...")

def summary(summary_m=False,summary_categ=None,summary_day=False):
    sql = ""
    header = ""

    if summary_m:
        header = "SUMMARY CATEGORY"
        sql = """SELECT categories.category,expenses.date,SUM(amount) as total_expense,AVG(amount) as average_expense,COUNT(*) as expense_count,
        CASE 
        WHEN AVG(amount) > 70 THEN 'HIGH'
        WHEN AVG(amount) > 45 THEN 'medium'
        ELSE 'Low'
        END expense_level
        FROM expenses
        LEFT JOIN categories
        ON expenses.category_id = categories.id
        GROUP BY categories.category,expenses.date"""
        with connect() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            if rows:
                print(header)
                print("="*80)
                for row in rows:
                    print(f"""category : {row["category"]}
        total_expense : {row["total_expense"]}
        average_expense : {row["average_expense"]}
        expense_count : {row["expense_count"]}
        expense_level : {row["expense_level"]}
        date : {row["date"]}
        """)
            else:
                print("NO CATEGORY FOUND...")

    if summary_categ:
        header = f"LOAD BY CATEGORY {summary_categ}"
        sql = """SELECT categories.category,expenses.date,SUM(amount) as total_expense,AVG(amount) as average_expense,COUNT(*) as expense_count,
        CASE 
        WHEN AVG(amount) > 70 THEN 'HIGH'
        WHEN AVG(amount) > 45 THEN 'medium'
        ELSE 'Low'
        END expense_level
        FROM expenses
        LEFT JOIN categories
        ON expenses.category_id = categories.id
        GROUP BY categories.category,expenses.date
        HAVING categories.category ILIKE %s"""

        with connect() as cur:
            cur.execute(sql,(summary_categ,))
            rows = cur.fetchall()
            if rows:
                print(header)
                print("="*80)
                
                for row in rows:
                    print(f"""category : {row["category"]}
        total_expense : {row["total_expense"]}
        average_expense : {row["average_expense"]}
        expense_count : {row["expense_count"]}
        expense_level : {row["expense_level"]}
        date : {row["date"]}
        """)
            else:
                print("NO CATEGORY FOUND...")
            
    if summary_day:
        header = "SUMMARY DATE"
        sql = """SELECT expenses.created_at::date AS date,categories.category,SUM(amount) as total_expense,AVG(amount) as average_expense,COUNT(*) as expense_count,
        CASE 
        WHEN AVG(amount) > 70 THEN 'HIGH'
        WHEN AVG(amount) > 45 THEN 'medium'
        ELSE 'Low'
        END expense_level
        FROM expenses
        LEFT JOIN categories
        ON expenses.category_id = categories.id
        GROUP BY expenses.created_at::date,categories.category"""

        with connect() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            if rows:
                print(header)
                print("="*80)
                for row in rows:
                    print(f"""date : {row["date"]}
        category : {row["category"]}
        total_expense : {row["total_expense"]}
        average_expense : {row["average_expense"]}
        expense_count : {row["expense_count"]}
""")

            else:
                print("NO CATEGORY FOUND...")

if __name__ == "__main__":
    init_db()
    #drop_table()
    #add_expense(25.30,"Paid phone bills")
    #display_expense()
    #update_expense(expense_id=5,description="by the way,What a stressfull day, I paid the house bills today,thers still food to stockup and also a vacation to dubai waiting")
    #delete_expense(4)
    #get_expenses()
    #load_expense(12)
    summary(summary_day=True)