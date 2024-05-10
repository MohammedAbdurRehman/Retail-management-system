import tkinter as tk
from tkinter import messagebox
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
except psycopg2.Error as e:
    messagebox.showerror(title="Database Connection Error", message=f"Error connecting to PostgreSQL: {e}")
    exit()

def create_order_product_table():
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Order_Product (
                OrderProduct_ID VARCHAR(100) PRIMARY KEY,
                Order_ID VARCHAR(100) REFERENCES Orders(Order_ID),
                Product_ID VARCHAR(100) REFERENCES Product(ProductID),
                Quantity INT
            )
        """)
        conn.commit()
        messagebox.showinfo(title="Success", message="Order_Product table created successfully")
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error creating table: {e}")

def insert_order_product():
    try:
        order_product_id = order_product_id_entry.get()
        order_id = order_id_entry.get()
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        cur.execute("INSERT INTO Order_Product(OrderProduct_ID, Order_ID, Product_ID, Quantity) VALUES (%s, %s, %s, %s)",
                    (order_product_id, order_id, product_id, quantity))
        conn.commit()
        messagebox.showinfo(title="Success", message="Order_Product data inserted successfully")
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error inserting data: {e}")

def delete_order_product():
    try:
        order_product_id = order_product_id_entry.get()
        cur.execute("DELETE FROM Order_Product WHERE OrderProduct_ID = %s", (order_product_id,))
        conn.commit()
        messagebox.showinfo(title="Success", message="Order_Product deleted successfully")
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error deleting data: {e}")

def view_order_products():
    try:
        cur.execute("SELECT * FROM Order_Product")
        rows = cur.fetchall()
        if rows:
            order_product_records = ""
            for row in rows:
                order_product_records += f"OrderProduct ID: {row[0]}, Order ID: {row[1]}, Product ID: {row[2]}, Quantity: {row[3]}\n"
            messagebox.showinfo(title="Order_Product Records", message=order_product_records)
        else:
            messagebox.showinfo(title="Order_Product Records", message="No order product records found")
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror(title="PostgreSQL Error", message=f"Error fetching data: {e}")

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

# Insert Order Product Button
insert_order_product_button = tk.Button(order_product_frame, text="Insert Order Product", command=insert_order_product)
insert_order_product_button.grid(row=4, column=0)

# OrderProduct ID for deletion
tk.Label(order_product_frame, text="OrderProduct ID for Deletion:").grid(row=5, column=0)
order_product_id_entry = tk.Entry(order_product_frame)
order_product_id_entry.grid(row=5, column=1)

# Delete Order Product Button
delete_order_product_button = tk.Button(order_product_frame, text="Delete Order Product", command=delete_order_product)
delete_order_product_button.grid(row=6, column=0)

# View Order Products Button
view_order_products_button = tk.Button(order_product_frame, text="View Order Products", command=view_order_products)
view_order_products_button.grid(row=4, column=1)

# Create the order product table if not exists
create_order_product_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
