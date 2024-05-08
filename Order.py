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

def insert_order():
    # Insert data into PostgreSQL
    insert_order_postgres()

    # Insert data into Firebase
    insert_order_firestore()

def delete_order():
    # Delete data from PostgreSQL
    delete_order_postgres()

    # Delete data from Firebase
    delete_order_firestore()

def create_order_table_postgres():
    # Create an order table in PostgreSQL
    cur_postgres.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id SERIAL PRIMARY KEY,
            shippment_duration VARCHAR(50),
            order_date DATE,
            status VARCHAR(50)
        )
    """)
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Order table created successfully")

def insert_order_postgres():
    # Insert data into the order table in PostgreSQL
    shipment_duration = shipment_duration_entry.get()
    order_date = order_date_entry.get()
    status = status_entry.get()
    cur_postgres.execute("INSERT INTO orders (shippment_duration, order_date, status) VALUES (%s, %s, %s)",
                (shipment_duration, order_date, status))
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Order data inserted successfully")

def delete_order_postgres():
    # Delete order from the order table in PostgreSQL
    order_id = order_id_entry.get()
    cur_postgres.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn_postgres.commit()
    messagebox.showinfo("Success", "PostgreSQL Order deleted successfully")

def insert_order_firestore():
    # Insert data into the order collection in Firestore
    shipment_duration = shipment_duration_entry.get()
    order_date = order_date_entry.get()
    status = status_entry.get()

    data = {
        'shipment_duration': shipment_duration,
        'order_date': order_date,
        'status': status
    }

    doc_ref = db_firestore.collection('orders').add(data)
    messagebox.showinfo("Success", "Firebase Order data inserted successfully")

def delete_order_firestore():
    # Delete order document from the orders collection in Firestore
    order_id = order_id_entry.get()
    db_firestore.collection('orders').document(order_id).delete()
    messagebox.showinfo("Success", "Firebase Order deleted successfully")

# Create the main window
window = tk.Tk()
window.title("Order Management")

# Create order management frame
order_frame = tk.Frame(window)
order_frame.pack(padx=20, pady=20)

# Shipment Duration
tk.Label(order_frame, text="Shipment Duration:").grid(row=0, column=0)
shipment_duration_entry = tk.Entry(order_frame)
shipment_duration_entry.grid(row=0, column=1)

# Order Date
tk.Label(order_frame, text="Order Date (YYYY-MM-DD):").grid(row=1, column=0)
order_date_entry = tk.Entry(order_frame)
order_date_entry.grid(row=1, column=1)

# Status
tk.Label(order_frame, text="Status:").grid(row=2, column=0)
status_entry = tk.Entry(order_frame)
status_entry.grid(row=2, column=1)

# Insert and Delete Order Buttons
order_button = tk.Button(order_frame, text="Insert/Delete Order", command=insert_order)
order_button.grid(row=3, columnspan=2, padx=5, pady=5)

# Order ID for deletion
tk.Label(order_frame, text="Order ID for Deletion:").grid(row=4, column=0)
order_id_entry = tk.Entry(order_frame)
order_id_entry.grid(row=4, column=1)

# Create the order table if not exists in PostgreSQL
create_order_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
