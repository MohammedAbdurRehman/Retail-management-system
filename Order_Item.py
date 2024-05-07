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

def create_order_item_table():
    # Create an order_item table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_item (
            orderitem_id SERIAL PRIMARY KEY,
            order_id INT,
            date_of_order DATE,
            quantity INT
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Order_Item table created successfully")

def insert_order_item():
    # Insert data into the order_item table
    order_id = order_id_entry.get()
    date_of_order = date_of_order_entry.get()
    quantity = quantity_entry.get()
    cur.execute("INSERT INTO order_item(order_id, date_of_order, quantity) VALUES (%s, %s, %s)",
                (order_id, date_of_order, quantity))
    conn.commit()
    messagebox.showinfo("Success", "Order_Item data inserted successfully")

def delete_order_item():
    # Delete order_item from the order_item table
    orderitem_id = orderitem_id_entry.get()
    cur.execute("DELETE FROM order_item WHERE orderitem_id = %s", (orderitem_id,))
    conn.commit()
    messagebox.showinfo("Success", "Order_Item deleted successfully")

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

# Insert Order_Item Button
insert_order_item_button = tk.Button(order_item_frame, text="Insert Order_Item", command=insert_order_item)
insert_order_item_button.grid(row=3, columnspan=2)

# Order_Item ID for deletion
tk.Label(order_item_frame, text="Order_Item ID for Deletion:").grid(row=4, column=0)
orderitem_id_entry = tk.Entry(order_item_frame)
orderitem_id_entry.grid(row=4, column=1)

# Delete Order_Item Button
delete_order_item_button = tk.Button(order_item_frame, text="Delete Order_Item", command=delete_order_item)
delete_order_item_button.grid(row=5, columnspan=2)

# Create the order_item table if not exists
create_order_item_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
