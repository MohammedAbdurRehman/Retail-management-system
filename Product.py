import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_product_table():
    # Create a products table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            productid SERIAL PRIMARY KEY,
            product_name VARCHAR(100),
            available_number INTEGER
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Product table created successfully")

def insert_product():
    # Insert data into the products table
    name = product_name_entry.get()
    quantity = product_quantity_entry.get()
    cur.execute("INSERT INTO products (product_name, available_number) VALUES (%s, %s)", (name, quantity))
    conn.commit()
    messagebox.showinfo("Success", "Product data inserted successfully")

def delete_product():
    # Delete product from the products table
    product_id = product_id_entry.get()
    cur.execute("DELETE FROM product WHERE productid = %s", (product_id,))
    conn.commit()
    messagebox.showinfo("Success", "Product deleted successfully")

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

# Insert Product Button
insert_product_button = tk.Button(product_frame, text="Insert Product", command=insert_product)
insert_product_button.grid(row=2, columnspan=2)

# Product ID for deletion
tk.Label(product_frame, text="Product ID for Deletion:").grid(row=3, column=0)
product_id_entry = tk.Entry(product_frame)
product_id_entry.grid(row=3, column=1)

# Delete Product Button
delete_product_button = tk.Button(product_frame, text="Delete Product", command=delete_product)
delete_product_button.grid(row=4, columnspan=2)

# Create the products table if not exists
create_product_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
