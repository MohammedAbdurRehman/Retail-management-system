import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

# Connect to PostgreSQL
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
    messagebox.showerror(title="Database Connection Error", message=f"Error connecting to PostgreSQL: {e}")
    exit()

def insert_order_product_postgres():
    try:
        order_product_id = order_product_id_entry.get()
        order_id = order_id_entry.get()
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        cur_postgres.execute("INSERT INTO Order_Product(OrderProduct_ID, Order_ID, Product_ID, Quantity) VALUES (%s, %s, %s, %s)",
                             (order_product_id, order_id, product_id, quantity))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="Data inserted successfully into PostgreSQL")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error inserting data: {e}")

def insert_order_product_firestore():
    try:
        order_product_id = order_product_id_entry.get()
        order_id = order_id_entry.get()
        product_id = product_id_entry.get()
        quantity = int(quantity_entry.get())
        db_firestore.collection('Order_Product').document(order_product_id).set({
            'Order_ID': order_id,
            'Product_ID': product_id,
            'Quantity': quantity
        })
        messagebox.showinfo(title="Success", message="Data inserted successfully into Firestore")
    except Exception as e:
        messagebox.showerror(title="Firestore Error", message=f"Error inserting data: {e}")

def delete_order_product_postgres():
    try:
        order_product_id = order_product_id_entry.get()
        cur_postgres.execute("DELETE FROM Order_Product WHERE OrderProduct_ID = %s", (order_product_id,))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="Data deleted successfully from PostgreSQL")
    except psycopg2.Error as e:
        conn_postgres.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error deleting data: {e}")

def delete_order_product_firestore():
    try:
        order_product_id = order_product_id_entry.get()
        db_firestore.collection('Order_Product').document(order_product_id).delete()
        messagebox.showinfo(title="Success", message="Data deleted successfully from Firestore")
    except Exception as e:
        messagebox.showerror(title="Firestore Error", message=f"Error deleting data: {e}")

def view_order_products_postgres():
    try:
        cur_postgres.execute("SELECT * FROM Order_Product")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Order Product Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("OrderProduct ID", "Order ID", "Product ID", "Quantity"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="OrderProduct ID")
            tree.heading("#2", text="Order ID")
            tree.heading("#3", text="Product ID")
            tree.heading("#4", text="Quantity")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Order Product Records", message="No order product records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def view_order_products_firestore():
    try:
        docs = db_firestore.collection('Order_Product').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Order Product Records (Firestore)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("OrderProduct ID", "Order ID", "Product ID", "Quantity"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="OrderProduct ID")
            tree.heading("#2", text="Order ID")
            tree.heading("#3", text="Product ID")
            tree.heading("#4", text="Quantity")

            for i, doc in enumerate(docs):
                order_data = doc.to_dict()
                order_values = (
                    doc.id,
                    order_data['Order_ID'],
                    order_data['Product_ID'],
                    order_data['Quantity']
                )
                tree.insert("", tk.END, text=str(i+1), values=order_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Order Product Records", message="No order product records found in Firestore")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firestore: {e}")
def insert_order_product():
    insert_order_product_postgres()
    insert_order_product_firestore()

def delete_order_product():
    delete_order_product_postgres()
    delete_order_product_firestore()

def view_order_product():
    view_order_products_postgres()
    view_order_products_firestore()

# Create the main window
window = tk.Tk()
window.title("Order Product Management")

# Create order product management frame
order_product_frame = tk.Frame(window)
order_product_frame.pack(padx=20, pady=20)

# OrderProduct ID
tk.Label(order_product_frame, text="OrderProduct ID:").grid(row=0, column=0)
order_product_id_entry = tk.Entry(order_product_frame)
order_product_id_entry.grid(row=0, column=1)

# Order ID
tk.Label(order_product_frame, text="Order ID:").grid(row=1, column=0)
order_id_entry = tk.Entry(order_product_frame)
order_id_entry.grid(row=1, column=1)

# Product ID
tk.Label(order_product_frame, text="Product ID:").grid(row=2, column=0)
product_id_entry = tk.Entry(order_product_frame)
product_id_entry.grid(row=2, column=1)

# Quantity
tk.Label(order_product_frame, text="Quantity:").grid(row=3, column=0)
quantity_entry = tk.Entry(order_product_frame)
quantity_entry.grid(row=3, column=1)

# PostgreSQL and Firestore Insert Buttons
tk.Button(order_product_frame, text="Insert Order Product", command=insert_order_product()).grid(row=4, column=0)

# PostgreSQL and Firestore Delete Buttons
tk.Button(order_product_frame, text="Delete Order Product", command=delete_order_product).grid(row=5)

# PostgreSQL and Firestore View Buttons
tk.Button(order_product_frame, text="View Order Product", command=view_order_product).grid(row=4, column=1)

# Run the main loop
window.mainloop()

# Close the database connections
cur_postgres.close()
conn_postgres.close()
