import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()

# Connect to your PostgreSQL database
try:
    conn_postgres = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur_postgres = conn_postgres.cursor()
except psycopg2.Error as e:
    messagebox.showerror(title="Error", message=f"Error connecting to PostgreSQL: {e}")

def create_voucher_table_postgres():
    try:
        # Create a voucher table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS Voucher (
                Voucher_number VARCHAR(20) PRIMARY KEY,
                Discount_percent INT
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Voucher table created successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error creating voucher table in PostgreSQL: {e}")

def insert_voucher_postgres():
    try:
        # Insert data into the voucher table in PostgreSQL
        voucher_id = voucher_id_entry.get()
        discount_percent = discount_percent_entry.get()
        cur_postgres.execute("INSERT INTO Voucher(Voucher_number, Discount_percent) VALUES (%s, %s)",
                    (voucher_id, discount_percent))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Voucher data inserted successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error inserting data into PostgreSQL: {e}")

def delete_voucher_postgres():
    try:
        # Delete voucher from the voucher table in PostgreSQL
        voucher_id = delete_voucher_id_entry.get()
        cur_postgres.execute("DELETE FROM Voucher WHERE Voucher_number = %s", (voucher_id,))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Voucher deleted successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error deleting voucher from PostgreSQL: {e}")

def view_vouchers_postgres():
    try:
        cur_postgres.execute("SELECT * FROM Voucher")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Voucher Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Voucher ID", "Discount Percent"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Voucher ID")
            tree.heading("#2", text="Discount Percent")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Voucher Records", message="No voucher records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def insert_voucher_firestore():
    try:
        # Insert data into the voucher collection in Firebase
        voucher_id = voucher_id_entry.get()
        discount_percent = discount_percent_entry.get()

        data = {
            'Discount_percent': int(discount_percent)
        }

        db_firestore.collection('vouchers').document(voucher_id).set(data)
        messagebox.showinfo(title="Success", message="Firebase Voucher data inserted successfully")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error inserting data into Firebase: {e}")

def delete_voucher_firestore():
    try:
        # Delete voucher from the voucher collection in Firebase
        voucher_id = delete_voucher_id_entry.get()
        db_firestore.collection('vouchers').document(voucher_id).delete()
        messagebox.showinfo(title="Success", message="Firebase Voucher deleted successfully")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error deleting voucher from Firebase: {e}")

def view_vouchers_firestore():
    try:
        docs = db_firestore.collection('vouchers').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Voucher Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Voucher ID", "Discount Percent"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Voucher ID")
            tree.heading("#2", text="Discount Percent")

            for i, doc in enumerate(docs):
                voucher_data = doc.to_dict()
                voucher_values = (
                    doc.id,
                    voucher_data['Discount_percent']
                )
                tree.insert("", tk.END, text=str(i+1), values=voucher_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Voucher Records", message="No voucher records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")

# Create the main window
window = tk.Tk()
window.title("Voucher Management")

# Create voucher management frame
voucher_frame = tk.Frame(window)
voucher_frame.pack(padx=20, pady=20)

# Voucher ID
tk.Label(voucher_frame, text="Voucher ID:").grid(row=0, column=0)
voucher_id_entry = tk.Entry(voucher_frame)
voucher_id_entry.grid(row=0, column=1)

# Discount Percent
tk.Label(voucher_frame, text="Discount Percent:").grid(row=1, column=0)
discount_percent_entry = tk.Entry(voucher_frame)
discount_percent_entry.grid(row=1, column=1)

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_voucher_postgres()
    insert_voucher_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_voucher_postgres()
    delete_voucher_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_vouchers_postgres()
    view_vouchers_firestore()

# Perform Operations Button
perform_operations_button = tk.Button(voucher_frame, text="Insert Voucher", command=perform_operations)
perform_operations_button.grid(row=2, column=0)

# Delete Voucher Button
delete_voucher_button = tk.Button(voucher_frame, text="Delete Voucher", command=delete_data)
delete_voucher_button.grid(row=2, column=1)

# View Vouchers Button
view_vouchers_button = tk.Button(voucher_frame, text="View Vouchers", command=view_data)
view_vouchers_button.grid(row=2, column=2)

# Create the voucher table if not exists in PostgreSQL
create_voucher_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
