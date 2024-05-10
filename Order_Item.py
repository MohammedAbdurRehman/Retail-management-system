import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
    messagebox.showerror(title="PostgreSQL Connection Error", message=f"Error connecting to PostgreSQL: {e}")
    exit()

# Initialize Firebase Admin
try:
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except Exception as e:
    messagebox.showerror(title="Firebase Initialization Error", message=f"Error initializing Firebase: {e}")
    exit()

def insert_order_item_postgres():
    # Insert data into the order_item table in PostgreSQL
    try:
        order_id = order_id_entry.get()
        date_of_order = date_of_order_entry.get()
        quantity = quantity_entry.get()
        cur_postgres.execute("INSERT INTO order_item(order_id, date_of_order, quantity) VALUES (%s, %s, %s)",
                    (order_id, date_of_order, quantity))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Order_Item data inserted successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error inserting data into PostgreSQL: {e}")

def delete_order_item_postgres():
    # Delete order_item from the order_item table in PostgreSQL
    try:
        orderitem_id = orderitem_id_entry.get()
        cur_postgres.execute("DELETE FROM order_item WHERE orderitem_id = %s", (orderitem_id,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Order_Item deleted successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error deleting data from PostgreSQL: {e}")

def insert_order_item_firestore():
    # Insert data into the order_item collection in Firestore
    try:
        order_id = order_id_entry.get()
        date_of_order = date_of_order_entry.get()
        quantity = quantity_entry.get()

        data = {
            'order_id': order_id,
            'date_of_order': date_of_order,
            'quantity': quantity
        }

        doc_ref = db_firestore.collection('order_item').add(data)
        messagebox.showinfo("Success", "Firebase Order_Item data inserted successfully")
    except Exception as e:
        messagebox.showerror(title="Firebase Error", message=f"Error inserting data into Firestore: {e}")

def delete_order_item_firestore():
    # Delete order_item document from the order_item collection in Firestore
    try:
        orderitem_id = orderitem_id_entry.get()
        db_firestore.collection('order_item').document(orderitem_id).delete()
        messagebox.showinfo("Success", "Firebase Order_Item deleted successfully")
    except Exception as e:
        messagebox.showerror(title="Firebase Error", message=f"Error deleting data from Firestore: {e}")

def create_order_item_table_postgres():
    # Create an order_item table in PostgreSQL
    try:
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS order_item (
                orderitem_id SERIAL PRIMARY KEY,
                order_id INT,
                date_of_order DATE,
                quantity INT
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Order_Item table created successfully")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error creating table in PostgreSQL: {e}")

def insert_data():
    insert_order_item_postgres()
    insert_order_item_firestore()
# Create the main window
window = tk.Tk()
window.title("Order_Item Management")

# Create order_item management frame
order_item_frame = tk.Frame(window)
order_item_frame.pack(padx=20, pady=20)

# Order ID
tk.Label(order_item_frame, text="Order ID:").grid(row=0, column=0)
order_id_entry = tk.Entry(order_item_frame)
order_id_entry.grid(row=0, column=1)

# Date of Order
tk.Label(order_item_frame, text="Date of Order (YYYY-MM-DD):").grid(row=1, column=0)
date_of_order_entry = tk.Entry(order_item_frame)
date_of_order_entry.grid(row=1, column=1)

# Quantity
tk.Label(order_item_frame, text="Quantity:").grid(row=2, column=0)
quantity_entry = tk.Entry(order_item_frame)
quantity_entry.grid(row=2, column=1)

# Insert/Delete Order_Item Button
manage_order_item_button = tk.Button(order_item_frame, text="Insert/Delete Order_Item", command=insert_data)
manage_order_item_button.grid(row=3, columnspan=2)

# Order_Item ID for deletion
tk.Label(order_item_frame, text="Order_Item ID for Deletion:").grid(row=4, column=0)
orderitem_id_entry = tk.Entry(order_item_frame)
orderitem_id_entry.grid(row=4, column=1)

# Create the order_item table if not exists in PostgreSQL
create_order_item_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
