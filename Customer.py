import tkinter as tk
from tkinter import messagebox,ttk
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

try:
    # Initialize PostgreSQL connection
    conn_postgres = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur_postgres = conn_postgres.cursor()

    # Initialize Firebase Admin
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except Exception as e:
    messagebox.showerror("Initialization Error", f"An error occurred during initialization: {e}")
    exit()

def insert_data():
    try:
        # Insert data into PostgreSQL
        insert_customer_postgres()

        # Insert data into Firebase
        create_customer_firestore()
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror("PostgreSQL Error", f"Failed to insert data: {e}")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Failed to insert data to Firebase: {e}")

def delete_data():
    try:
        # Delete data from PostgreSQL
        delete_customer_postgres()

        # Delete data from Firebase
        delete_customer_firestore()
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror("PostgreSQL Error", f"Failed to delete data: {e}")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Failed to delete data from Firebase: {e}")

def create_customer_table_postgres():
    try:
        # Create a customer table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                customerid SERIAL PRIMARY KEY NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                mail_address VARCHAR(100),
                phone_number VARCHAR(20),
                category VARCHAR(50)
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Customer table created successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror("PostgreSQL Error", f"Failed to create Customer table: {e}")

def insert_customer_postgres():
    try:
        # Insert data into the customer table in PostgreSQL
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        mail_address = mail_address_entry.get()
        phone_number = phone_number_entry.get()
        category = category_entry.get()
        cur_postgres.execute("INSERT INTO customer (first_name, last_name, mail_address, phone_number, category) VALUES (%s, %s, %s, %s, %s)",
                    (first_name, last_name, mail_address, phone_number, category))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Customer data inserted successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror("PostgreSQL Error", f"Failed to insert Customer data: {e}")

def delete_customer_postgres():
    try:
        # Delete customer from the customer table in PostgreSQL
        customer_id = customer_id_entry.get()
        cur_postgres.execute("DELETE FROM customer WHERE customerid = %s", (customer_id,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Customer deleted successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror("PostgreSQL Error", f"Failed to delete Customer: {e}")

def create_customer_firestore():
    try:
        # Create a customer document in Firestore
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        mail_address = mail_address_entry.get()
        phone_number = phone_number_entry.get()
        category = category_entry.get()

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'mail_address': mail_address,
            'phone_number': phone_number,
            'category': category
        }

        doc_ref = db_firestore.collection('customers').add(data)
        messagebox.showinfo("Success", "Firebase Customer data inserted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Failed to insert Customer data to Firebase: {e}")

def delete_customer_firestore():
    try:
        # Delete customer document from Firestore
        customer_id = customer_id_entry.get()
        db_firestore.collection('customers').document(customer_id).delete()
        messagebox.showinfo("Success", "Firebase Customer deleted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Failed to delete Customer from Firebase: {e}")

def view_customers_postgres():
    try:
        cur_postgres.execute("SELECT * FROM customer")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Customer Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Customer ID", "First Name", "Last Name", "Mail Address", "Phone Number", "Category"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Customer ID")
            tree.heading("#2", text="First Name")
            tree.heading("#3", text="Last Name")
            tree.heading("#4", text="Mail Address")
            tree.heading("#5", text="Phone Number")
            tree.heading("#6", text="Category")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Customer Records", message="No customer records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def view_customers_firestore():
    try:
        docs = db_firestore.collection('customers').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Customer Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Customer ID", "First Name", "Last Name", "Mail Address", "Phone Number", "Category"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Customer ID")
            tree.heading("#2", text="First Name")
            tree.heading("#3", text="Last Name")
            tree.heading("#4", text="Mail Address")
            tree.heading("#5", text="Phone Number")
            tree.heading("#6", text="Category")

            for i, doc in enumerate(docs):
                customer_data = doc.to_dict()
                customer_values = (
                    doc.id,
                    customer_data['first_name'],
                    customer_data['last_name'],
                    customer_data['mail_address'],
                    customer_data['phone_number'],
                    customer_data['category']
                )
                tree.insert("", tk.END, text=str(i+1), values=customer_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Customer Records", message="No customer records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")

def view_data():
    view_customers_postgres()
    view_customers_firestore()


# Create the main window
window = tk.Tk()
window.title("Customer Management")

# Create customer management frame
customer_frame = tk.Frame(window)
customer_frame.pack(padx=20, pady=20)

# First Name
tk.Label(customer_frame, text="First Name:").grid(row=0, column=0)
first_name_entry = tk.Entry(customer_frame)
first_name_entry.grid(row=0, column=1)

# Last Name
tk.Label(customer_frame, text="Last Name:").grid(row=1, column=0)
last_name_entry = tk.Entry(customer_frame)
last_name_entry.grid(row=1, column=1)

# Mail Address
tk.Label(customer_frame, text="Mail Address:").grid(row=2, column=0)
mail_address_entry = tk.Entry(customer_frame)
mail_address_entry.grid(row=2, column=1)

# Phone Number
tk.Label(customer_frame, text="Phone Number:").grid(row=3, column=0)
phone_number_entry = tk.Entry(customer_frame)
phone_number_entry.grid(row=3, column=1)

# Category
tk.Label(customer_frame, text="Category:").grid(row=4, column=0)
category_entry = tk.Entry(customer_frame)
category_entry.grid(row=4, column=1)

# Insert and Delete Buttons
insert_button = tk.Button(customer_frame, text="Insert Data", command=insert_data)
insert_button.grid(row=5, column=0, padx=5, pady=5)
delete_button = tk.Button(customer_frame, text="Delete Data", command=delete_data)
delete_button.grid(row=7, column=0, padx=5, pady=5)

# Customer ID for deletion
tk.Label(customer_frame, text="Customer ID for Deletion:").grid(row=6, column=0)
customer_id_entry = tk.Entry(customer_frame)
customer_id_entry.grid(row=6, column=1)

# View Data Button
view_data_button = tk.Button(customer_frame, text="View Data", command=view_data)
view_data_button.grid(row=5, column=1, columnspan=2, pady=10)

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
if cur_postgres:
    cur_postgres.close()
if conn_postgres:
    conn_postgres.close()
