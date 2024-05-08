import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

def insert_data():
    # Insert data into PostgreSQL
    insert_customer_postgres()

    # Insert data into Firebase
    create_customer_firestore()

def delete_data():
    # Delete data from PostgreSQL
    delete_customer_postgres()

    # Delete data from Firebase
    delete_customer_firestore()

def create_customer_table_postgres():
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

def insert_customer_postgres():
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

def delete_customer_postgres():
    # Delete customer from the customer table in PostgreSQL
    customer_id = customer_id_entry.get()
    cur_postgres.execute("DELETE FROM customer WHERE customerid = %s", (customer_id,))
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Customer deleted successfully")

def create_customer_firestore():
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

def delete_customer_firestore():
    # Delete customer document from Firestore
    customer_id = customer_id_entry.get()
    db_firestore.collection('customers').document(customer_id).delete()
    messagebox.showinfo("Success", "Firebase Customer deleted successfully")

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
delete_button.grid(row=5, column=1, padx=5, pady=5)

# Customer ID for deletion
tk.Label(customer_frame, text="Customer ID for Deletion:").grid(row=6, column=0)
customer_id_entry = tk.Entry(customer_frame)
customer_id_entry.grid(row=6, column=1)

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
