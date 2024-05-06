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

def create_customer_table():
    # Create a customer table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customerid SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            mail_address VARCHAR(100),
            phone_number VARCHAR(20),
            category VARCHAR(50)
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Customer table created successfully")

def insert_customer():
    # Insert data into the customer table
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    mail_address = mail_address_entry.get()
    phone_number = phone_number_entry.get()
    category = category_entry.get()
    cur.execute("INSERT INTO customer (first_name, last_name, mail_address, phone_number, category) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, mail_address, phone_number, category))
    conn.commit()
    messagebox.showinfo("Success", "Customer data inserted successfully")

def delete_customer():
    # Delete customer from the customer table
    customer_id = customer_id_entry.get()
    cur.execute("DELETE FROM customer WHERE customerid = %s", (customer_id,))
    conn.commit()
    messagebox.showinfo("Success", "Customer deleted successfully")

# Create the main window
window = tk.Tk()
window.title("Customer Management")

# Create customer management frame
customer_frame = tk.Frame(window)
customer_frame.pack(padx=20, pady=20)

# First Name
tk.Label(customer_frame, text="First Name:").grid(row=0, column=0)
first_name_entry = tk.Entry(customer_frame)
first_name_entry.grid(row=0, column=1)

# Last Name
tk.Label(customer_frame, text="Last Name:").grid(row=1, column=0)
last_name_entry = tk.Entry(customer_frame)
last_name_entry.grid(row=1, column=1)

# Mail Address
tk.Label(customer_frame, text="Mail Address:").grid(row=2, column=0)
mail_address_entry = tk.Entry(customer_frame)
mail_address_entry.grid(row=2, column=1)

# Phone Number
tk.Label(customer_frame, text="Phone Number:").grid(row=3, column=0)
phone_number_entry = tk.Entry(customer_frame)
phone_number_entry.grid(row=3, column=1)

# Category
tk.Label(customer_frame, text="Category:").grid(row=4, column=0)
category_entry = tk.Entry(customer_frame)
category_entry.grid(row=4, column=1)

# Insert Customer Button
insert_customer_button = tk.Button(customer_frame, text="Insert Customer", command=insert_customer)
insert_customer_button.grid(row=5, columnspan=2)

# Customer ID for deletion
tk.Label(customer_frame, text="Customer ID for Deletion:").grid(row=6, column=0)
customer_id_entry = tk.Entry(customer_frame)
customer_id_entry.grid(row=6, column=1)

# Delete Customer Button
delete_customer_button = tk.Button(customer_frame, text="Delete Customer", command=delete_customer)
delete_customer_button.grid(row=7, columnspan=2)

# Create the customer table if not exists
create_customer_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
