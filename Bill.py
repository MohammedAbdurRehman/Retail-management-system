import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
try:
    # Connect to your PostgreSQL database
    conn_postgres = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur_postgres = conn_postgres.cursor()
except psycopg2.Error as e:
    messagebox.showinfo(title="Error", message=f"Error connecting database: {e}")
# Initialize Firebase Admin
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()

def create_bill_table_postgres():
    try:
        # Create a bill table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS bill (
                billing_id SERIAL PRIMARY KEY,
                amount_paid NUMERIC(10, 2)
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Bill table created successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error creating bill table: {e}")

def insert_bill_postgres():
    try:
        # Insert data into the bill table in PostgreSQL
        amount_paid = amount_paid_entry.get()
        cur_postgres.execute("INSERT INTO bill (amount_paid) VALUES (%s)", (amount_paid,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Bill data inserted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error inserting bill data: {e}")

def delete_bill_postgres():
    try:
        # Delete bill from the bill table in PostgreSQL
        billing_id = billing_id_entry.get()
        cur_postgres.execute("DELETE FROM bill WHERE billing_id = %s", (billing_id,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Bill deleted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error deleting bill: {e}")

def view_bills_postgres():
    try:
        # View bills from the bill table in PostgreSQL
        cur_postgres.execute("SELECT * FROM bill")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Bill Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Billing ID", "Amount Paid"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Billing ID")
            tree.heading("#2", text="Amount Paid")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Bill Records", message="No bill records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def view_bills_firestore():
    try:
        # View bills from the bill collection in Firebase
        docs = db_firestore.collection('bills').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Bill Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Billing ID", "Amount Paid"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Billing ID")
            tree.heading("#2", text="Amount Paid")

            for i, doc in enumerate(docs):
                bill_data = doc.to_dict()
                bill_values = (
                    doc.id,
                    bill_data['amount_paid']
                )
                tree.insert("", tk.END, text=str(i+1), values=bill_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Bill Records", message="No bill records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")


def insert_bill_firestore():
    try:
        # Insert data into the bill collection in Firebase
        amount_paid = amount_paid_entry.get()

        data = {
            'amount_paid': amount_paid
        }

        doc_ref = db_firestore.collection('bills').add(data)
        messagebox.showinfo("Success", "Firebase Bill data inserted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Error inserting bill data: {e}")

def delete_bill_firestore():
    try:
        # Delete bill from the bill collection in Firebase
        billing_id = billing_id_entry.get()
        db_firestore.collection('bills').document(billing_id).delete()
        messagebox.showinfo("Success", "Firebase Bill deleted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Error deleting bill: {e}")


# Create the main window
window = tk.Tk()
window.title("Bill Management")

# Create bill management frame
bill_frame = tk.Frame(window)
bill_frame.pack(padx=20, pady=20)

# Amount Paid
tk.Label(bill_frame, text="Amount Paid:").grid(row=0, column=0)
amount_paid_entry = tk.Entry(bill_frame)
amount_paid_entry.grid(row=0, column=1)

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_bill_postgres()
    insert_bill_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_bill_postgres()
    delete_bill_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_bills_postgres()
    view_bills_firestore()

# Insert/Delete/View Bill Button
manage_bill_button = tk.Button(bill_frame, text="Insert Bills", command=perform_operations)
manage_bill_button.grid(row=1, column=0)

# Delete Bill Button
delete_bill_button = tk.Button(bill_frame, text="Delete Bill", command=delete_data)
delete_bill_button.grid(row=1, column=1)

# View Bills Button
view_bills_button = tk.Button(bill_frame, text="View Bills", command=view_data)
view_bills_button.grid(row=1, column=2)

# Create the bill table if not exists in PostgreSQL
create_bill_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
