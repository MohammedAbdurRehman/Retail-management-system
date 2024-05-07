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

def create_product_details_table():
    # Create a product_details table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_details (
            productid SERIAL PRIMARY KEY,
            weight NUMERIC(10),
            width NUMERIC(10),
            colour VARCHAR(50),
            height NUMERIC(10)
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Product_Details table created successfully")

def insert_product_details():
    # Insert data into the product_details table
    productid = productid_entry.get()
    weight = weight_entry.get()
    width = width_entry.get()
    colour = colour_entry.get()
    height = height_entry.get()
    cur.execute("INSERT INTO product_details(productid, weight, width, colour, height) VALUES (%s, %s, %s, %s, %s)",
                (productid, weight, width, colour, height))
    conn.commit()
    messagebox.showinfo("Success", "Product_Details data inserted successfully")

def delete_product_details():
    # Delete product_details from the product_details table
    productid = productid_entry_del.get()
    cur.execute("DELETE FROM product_details WHERE productid = %s", (productid,))
    conn.commit()
    messagebox.showinfo("Success", "Product_Details deleted successfully")

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

# Insert Product_Details Button
insert_product_details_button = tk.Button(product_details_frame, text="Insert Product_Details", command=insert_product_details)
insert_product_details_button.grid(row=5, columnspan=2)

# Product_Details ID for deletion
tk.Label(product_details_frame, text="Product ID for Deletion:").grid(row=6, column=0)
productid_entry_del = tk.Entry(product_details_frame)
productid_entry_del.grid(row=6, column=1)

# Delete Product_Details Button
delete_product_details_button = tk.Button(product_details_frame, text="Delete Product_Details", command=delete_product_details)
delete_product_details_button.grid(row=7, columnspan=2)

# Create the product_details table if not exists
create_product_details_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
