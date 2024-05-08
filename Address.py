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

def create_address_table_postgres():
    # Create an address table in PostgreSQL
    cur_postgres.execute("""
        CREATE TABLE IF NOT EXISTS address (
            addressid SERIAL PRIMARY KEY,
            address_line1 VARCHAR(100),
            address_line2 VARCHAR(100)
        )
    """)
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Address table created successfully")

def insert_address_postgres():
    # Insert data into the address table in PostgreSQL
    address_line1 = address_line1_entry.get()
    address_line2 = address_line2_entry.get()
    cur_postgres.execute("INSERT INTO address (address_line1, address_line2) VALUES (%s, %s)",
                (address_line1, address_line2))
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Address data inserted successfully")

def delete_address_postgres():
    # Delete address from the address table in PostgreSQL
    address_id = address_id_entry.get()
    cur_postgres.execute("DELETE FROM address WHERE addressid = %s", (address_id,))
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Address deleted successfully")

def view_addresses_postgres():
    # View addresses from the address table in PostgreSQL
    cur_postgres.execute("SELECT * FROM address")
    rows = cur_postgres.fetchall()
    if rows:
        address_records = ""
        for row in rows:
            address_records += f"Address ID: {row[0]}, Line 1: {row[1]}, Line 2: {row[2]}\n"
        messagebox.showinfo("Address Records (PostgreSQL)", address_records)
    else:
        messagebox.showinfo("Address Records (PostgreSQL)", "No address records found in PostgreSQL")

def insert_address_firestore():
    # Insert data into the address collection in Firebase
    address_line1 = address_line1_entry.get()
    address_line2 = address_line2_entry.get()

    data = {
        'address_line1': address_line1,
        'address_line2': address_line2
    }

    doc_ref = db_firestore.collection('addresses').add(data)
    messagebox.showinfo("Success", "Firebase Address data inserted successfully")

def delete_address_firestore():
    # Delete address from the address collection in Firebase
    address_id = address_id_entry.get()
    db_firestore.collection('addresses').document(address_id).delete()
    messagebox.showinfo("Success", "Firebase Address deleted successfully")

def view_addresses_firestore():
    # View addresses from the address collection in Firebase
    docs = db_firestore.collection('addresses').stream()
    address_records = ""
    for doc in docs:
        address_data = doc.to_dict()
        address_records += f"Address ID: {doc.id}, Line 1: {address_data['address_line1']}, Line 2: {address_data['address_line2']}\n"
    if address_records:
        messagebox.showinfo("Address Records (Firebase)", address_records)
    else:
        messagebox.showinfo("Address Records (Firebase)", "No address records found in Firebase")

# Create the main window
window = tk.Tk()
window.title("Address Management")

# Create address management frame
address_frame = tk.Frame(window)
address_frame.pack(padx=20, pady=20)

# Address Line 1
tk.Label(address_frame, text="Address Line 1:").grid(row=0, column=0)
address_line1_entry = tk.Entry(address_frame)
address_line1_entry.grid(row=0, column=1)

# Address Line 2
tk.Label(address_frame, text="Address Line 2:").grid(row=1, column=0)
address_line2_entry = tk.Entry(address_frame)
address_line2_entry.grid(row=1, column=1)

def perform_operations():
    # Insert data into PostgreSQL
    insert_address_postgres()

    # Insert data into Firebase
    insert_address_firestore()

def delete_data():
    # Delete data from PostgreSQL
    delete_address_postgres()

    # Delete data from Firebase
    delete_address_firestore()

def view_data():
    # View data from PostgreSQL
    view_addresses_postgres()

    # View data from Firebase
    view_addresses_firestore()

# Insert/Delete/View Address Button
manage_address_button = tk.Button(address_frame, text="Insert Address", command=perform_operations)
manage_address_button.grid(row=2, column=0)

# Delete Address Button
delete_address_button = tk.Button(address_frame, text="Delete Address", command=delete_data)
delete_address_button.grid(row=2, column=1)

# View Addresses Button
view_addresses_button = tk.Button(address_frame, text="View Addresses", command=view_data)
view_addresses_button.grid(row=2, column=2)

# Create the address table if not exists in PostgreSQL
create_address_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
