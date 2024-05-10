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

def handle_error(message):
    messagebox.showerror(title="Error", message=message)

def insert_data():
    try:
        # Insert data into PostgreSQL
        insert_product_details_postgres()

        # Insert data into Firebase
        insert_product_details_firestore()
        messagebox.showinfo("Success", "Data inserted successfully")
    except psycopg2.Error as e:
        handle_error(f"PostgreSQL Error: {e}")
    except Exception as e:
        handle_error(f"Firebase Error: {e}")

def delete_data():
    try:
        # Delete data from PostgreSQL
        delete_product_details_postgres()

        # Delete data from Firebase
        delete_product_details_firestore()
        messagebox.showinfo("Success", "Data deleted successfully")
    except psycopg2.Error as e:
        handle_error(f"PostgreSQL Error: {e}")
    except Exception as e:
        handle_error(f"Firebase Error: {e}")

def create_product_details_table_postgres():
    try:
        # Create a product_details table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS product_details (
                productid SERIAL PRIMARY KEY,
                weight NUMERIC(10),
                width NUMERIC(10),
                colour VARCHAR(50),
                height NUMERIC(10)
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo("Success", "PostgreSQL Product_Details table created successfully")
    except psycopg2.Error as e:
        handle_error(f"PostgreSQL Error: {e}")

def insert_product_details_postgres():
    try:
        # Insert data into the product_details table in PostgreSQL
        productid = productid_entry.get()
        weight = weight_entry.get()
        width = width_entry.get()
        colour = colour_entry.get()
        height = height_entry.get()
        cur_postgres.execute("INSERT INTO product_details(productid, weight, width, colour, height) VALUES (%s, %s, %s, %s, %s)",
                    (productid, weight, width, colour, height))
        conn_postgres.commit()
    except psycopg2.Error as e:
        conn_postgres.rollback()
        raise e

def delete_product_details_postgres():
    try:
        # Delete product_details from the product_details table in PostgreSQL
        productid = productid_entry_del.get()
        cur_postgres.execute("DELETE FROM product_details WHERE productid = %s", (productid,))
        conn_postgres.commit()
    except psycopg2.Error as e:
        conn_postgres.rollback()
        raise e

def insert_product_details_firestore():
    try:
        # Insert data into the product_details collection in Firestore
        productid = productid_entry.get()
        weight = weight_entry.get()
        width = width_entry.get()
        colour = colour_entry.get()
        height = height_entry.get()

        data = {
            'productid': productid,
            'weight': weight,
            'width': width,
            'colour': colour,
            'height': height
        }

        doc_ref = db_firestore.collection('product_details').add(data)
    except Exception as e:
        raise e

def delete_product_details_firestore():
    try:
        # Delete product_details document from the product_details collection in Firestore
        productid = productid_entry_del.get()
        db_firestore.collection('product_details').document(productid).delete()
    except Exception as e:
        raise e

# Create the main window
window = tk.Tk()
window.title("Product_Details Management")

# Create product_details management frame
product_details_frame = tk.Frame(window)
product_details_frame.pack(padx=20, pady=20)

# Product ID
tk.Label(product_details_frame, text="Product ID:").grid(row=0, column=0)
productid_entry = tk.Entry(product_details_frame)
productid_entry.grid(row=0, column=1)

# Weight
tk.Label(product_details_frame, text="Weight:").grid(row=1, column=0)
weight_entry = tk.Entry(product_details_frame)
weight_entry.grid(row=1, column=1)

# Width
tk.Label(product_details_frame, text="Width:").grid(row=2, column=0)
width_entry = tk.Entry(product_details_frame)
width_entry.grid(row=2, column=1)

# Colour
tk.Label(product_details_frame, text="Colour:").grid(row=3, column=0)
colour_entry = tk.Entry(product_details_frame)
colour_entry.grid(row=3, column=1)

# Height
tk.Label(product_details_frame, text="Height:").grid(row=4, column=0)
height_entry = tk.Entry(product_details_frame)
height_entry.grid(row=4, column=1)

# Insert/Delete Product_Details Button
manage_product_details_button = tk.Button(product_details_frame, text="Insert/Delete Product_Details", command=insert_data)
manage_product_details_button.grid(row=5, columnspan=2)

# Product_Details ID for deletion
tk.Label(product_details_frame, text="Product ID for Deletion:").grid(row=6, column=0)
productid_entry_del = tk.Entry(product_details_frame)
productid_entry_del.grid(row=6, column=1)

# Create the product_details table if not exists in PostgreSQL
create_product_details_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
