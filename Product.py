import tkinter as tk
from tkinter import messagebox,ttk
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()


# Connect to your PostgreSQL database
conn_postgres = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)
cur_postgres = conn_postgres.cursor()

def create_product_table_postgres():
    try:
        # Create a products table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS product (
                productid SERIAL PRIMARY KEY,
                product_name VARCHAR(100),
                available_number INTEGER
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Product table created successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error creating product table: {e}")

def insert_product_postgres():
    try:
        # Insert data into the products table in PostgreSQL
        name = product_name_entry.get()
        quantity = product_quantity_entry.get()
        cur_postgres.execute("INSERT INTO product (product_name, available_number) VALUES (%s, %s)", (name, quantity))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Product data inserted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error inserting product data: {e}")

def delete_product_postgres():
    try:
        # Delete product from the products table in PostgreSQL
        product_id = product_id_entry.get()
        cur_postgres.execute("DELETE FROM product WHERE productid = %s", (product_id,))
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Product deleted successfully")
    except psycopg2.Error as e:
        messagebox.showerror("PostgreSQL Error", f"Error deleting product: {e}")


def insert_product_firestore():
    try:
        # Insert data into the products collection in Firebase
        name = product_name_entry.get()
        quantity = product_quantity_entry.get()

        data = {
            'product_name': name,
            'available_number': quantity
        }

        db_firestore.collection('products').add(data)
        messagebox.showinfo("Success", "Firebase Product data inserted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Error inserting product data: {e}")

def delete_product_firestore():
    try:
        # Delete product from the products collection in Firebase
        product_id = product_id_entry.get()
        db_firestore.collection('products').document(product_id).delete()
        messagebox.showinfo("Success", "Firebase Product deleted successfully")
    except Exception as e:
        messagebox.showerror("Firebase Error", f"Error deleting product: {e}")

def view_products_postgres():
    try:
        cur_postgres.execute("SELECT product_name, available_number FROM product")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Product Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Product Name", "Available Number"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Product Name")
            tree.heading("#2", text="Available Number")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Product Records", message="No product records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="PostgreSQL Error", message=f"Error viewing product records: {e}")

def view_products_firestore():
    try:
        docs = db_firestore.collection('products').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Product Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Product Name", "Available Number"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Product Name")
            tree.heading("#2", text="Available Number")

            for i, doc in enumerate(docs):
                product_data = doc.to_dict()
                product_values = (
                    product_data['product_name'],
                    product_data['available_number']
                )
                tree.insert("", tk.END, text=str(i+1), values=product_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Product Records", message="No product records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Firebase Error", message=f"Error viewing product records: {e}")


# Create the main window
window = tk.Tk()
window.title("Product Management")

# Create products management frame
product_frame = tk.Frame(window)
product_frame.pack(padx=20, pady=20)

# Product Name
tk.Label(product_frame, text="Product Name:").grid(row=0, column=0)
product_name_entry = tk.Entry(product_frame)
product_name_entry.grid(row=0, column=1)

# Available Number
tk.Label(product_frame, text="Available Number:").grid(row=1, column=0)
product_quantity_entry = tk.Entry(product_frame)
product_quantity_entry.grid(row=1, column=1)

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_product_postgres()
    insert_product_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_product_postgres()
    delete_product_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_products_postgres()
    view_products_firestore()

# Perform Operations Button
perform_operations_button = tk.Button(product_frame, text="Insert Product", command=perform_operations)
perform_operations_button.grid(row=2, column=0)

# Delete Product Button
delete_product_button = tk.Button(product_frame, text="Delete Product", command=delete_data)
delete_product_button.grid(row=2, column=1)

# View Products Button
view_products_button = tk.Button(product_frame, text="View Products", command=view_data)
view_products_button.grid(row=2, column=2)

# Create the products table if not exists in PostgreSQL
create_product_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
