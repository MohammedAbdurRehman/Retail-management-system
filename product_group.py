import tkinter as tk
from tkinter import messagebox,ttk
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2

# PostgreSQL connection setup
try:
    conn = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
except psycopg2.Error as e:
    messagebox.showerror("Database Connection Error", f"Failed to connect to database: {e}")

# Firebase setup
try:
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except Exception as e:
    messagebox.showerror(title="Firebase Connection Error", message=str(e))


def create_product_group_table():
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Product_Group (
                Group_ID SERIAL PRIMARY KEY,
                Group_Name VARCHAR(50)
            )
        """)
        conn.commit()
        messagebox.showinfo(title="Success", message="Product Group table created successfully in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Failed to create Product_Group table: {e}")
        conn.rollback()


def insert_product_group():
    group_name = group_name_entry.get()
    try:
        # PostgreSQL insertion
        cur.execute("INSERT INTO Product_Group(Group_Name) VALUES (%s) RETURNING Group_ID", (group_name,))
        group_id = cur.fetchone()[0]
        conn.commit()

        # Firebase insertion
        doc_ref = db_firestore.collection('Product_Group').document(str(group_id))
        doc_ref.set({'Group_Name': group_name})
        messagebox.showinfo(title="Success", message="Product group inserted successfully in both databases")
    except (psycopg2.Error, Exception) as e:
        messagebox.showerror("Insert Error", f"Failed to insert product group: {e}")
        conn.rollback()


def delete_product_group():
    group_id = group_id_entry.get()
    try:
        # PostgreSQL deletion
        cur.execute("DELETE FROM Product_Group WHERE Group_ID = %s", (group_id,))
        conn.commit()

        # Firebase deletion
        db_firestore.collection('Product_Group').document(group_id).delete()
        messagebox.showinfo(title="Success", message="Product group deleted successfully in both databases")
    except (psycopg2.Error, Exception) as e:
        messagebox.showerror("Delete Error", f"Failed to delete product group: {e}")
        conn.rollback()
def view_product_groups_postgres():
    try:
        cur.execute("SELECT Group_ID, Group_Name FROM Product_Group")
        rows = cur.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Product Group Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Group ID", "Group Name"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Group ID")
            tree.heading("#2", text="Group Name")

            tree.column("#1", width=100)
            tree.column("#2", width=200)

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i + 1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Product Group Records", message="No product group records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def view_product_groups_firestore():
    try:
        docs = db_firestore.collection('Product_Group').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Product Group Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Group ID", "Group Name"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Group ID")
            tree.heading("#2", text="Group Name")

            tree.column("#1", width=100)
            tree.column("#2", width=200)

            for i, doc in enumerate(docs):
                group_data = doc.to_dict()
                group_values = (
                    doc.id,
                    group_data.get('Group_Name', 'N/A')
                )
                tree.insert("", tk.END, text=str(i + 1), values=group_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Product Group Records", message="No product group records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")

def view_product_groups():
    view_product_groups_firestore()
    view_product_groups_postgres()


# GUI Setup
window = tk.Tk()
window.title("Product Group Management")
product_group_frame = tk.Frame(window)
product_group_frame.pack(padx=20, pady=20)

tk.Label(product_group_frame, text="Group Name:").grid(row=0, column=0)
group_name_entry = tk.Entry(product_group_frame)
group_name_entry.grid(row=0, column=1)

insert_product_group_button = tk.Button(product_group_frame, text="Insert Product Group", command=insert_product_group)
insert_product_group_button.grid(row=1, column=0)

tk.Label(product_group_frame, text="Group ID for Deletion:").grid(row=2, column=0)
group_id_entry = tk.Entry(product_group_frame)
group_id_entry.grid(row=2, column=1)

delete_product_group_button = tk.Button(product_group_frame, text="Delete Product Group", command=delete_product_group)
delete_product_group_button.grid(row=3, column=0)

view_product_groups_button = tk.Button(product_group_frame, text="View Product Groups", command=view_product_groups)
view_product_groups_button.grid(row=1, column=1)

create_product_group_table()
window.mainloop()

# Close database connection
if cur:
    cur.close()
if conn:
    conn.close()
