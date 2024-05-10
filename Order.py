import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize PostgreSQL connection
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
    messagebox.showerror("Error", f"Error connecting to PostgreSQL: {e}")

# Initialize Firebase Admin
try:
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except Exception as e:
    messagebox.showerror("Error", f"Error initializing Firebase Admin: {e}")

def insert_order():
    try:
        insert_order_postgres()
        insert_order_firestore()
    except Exception as e:
        messagebox.showerror("Error", f"Error inserting order: {e}")

def delete_order():
    try:
        delete_order_postgres()
        delete_order_firestore()
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting order: {e}")

def create_order_table_postgres():
    try:
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
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error creating order table: {e}")

def insert_order_postgres():
    try:
        shipment_duration = shipment_duration_entry.get()
        order_date = order_date_entry.get()
        status = status_entry.get()
        cur_postgres.execute("INSERT INTO orders (shippment_duration, order_date, status) VALUES (%s, %s, %s)",
                    (shipment_duration, order_date, status))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Order data inserted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error inserting order into PostgreSQL: {e}")

def delete_order_postgres():
    try:
        order_id = order_id_entry.get()
        cur_postgres.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Order deleted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error deleting order from PostgreSQL: {e}")

def insert_order_firestore():
    try:
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
    except Exception as e:
        messagebox.showerror("Error", f"Error inserting order into Firebase: {e}")

def delete_order_firestore():
    try:
        order_id = order_id_entry.get()
        db_firestore.collection('orders').document(order_id).delete()
        messagebox.showinfo("Success", "Firebase Order deleted successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting order from Firebase: {e}")

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
