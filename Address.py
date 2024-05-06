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

def create_address_table():
    # Create an address table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS address (
            addressid SERIAL PRIMARY KEY,
            address_line1 VARCHAR(100),
            address_line2 VARCHAR(100)
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Address table created successfully")

def insert_address():
    # Insert data into the address table
    address_line1 = address_line1_entry.get()
    address_line2 = address_line2_entry.get()
    cur.execute("INSERT INTO address (address_line1, address_line2) VALUES (%s, %s)",
                (address_line1, address_line2))
    conn.commit()
    messagebox.showinfo("Success", "Address data inserted successfully")

def delete_address():
    # Delete address from the address table
    address_id = address_id_entry.get()
    cur.execute("DELETE FROM address WHERE addressid = %s", (address_id,))
    conn.commit()
    messagebox.showinfo("Success", "Address deleted successfully")

# Create the main window
window = tk.Tk()
window.title("Address Management")

# Create address management frame
address_frame = tk.Frame(window)
address_frame.pack(padx=20, pady=20)

# Address Line 1
tk.Label(address_frame, text="Address Line 1:").grid(row=0, column=0)
address_line1_entry = tk.Entry(address_frame)
address_line1_entry.grid(row=0, column=1)

# Address Line 2
tk.Label(address_frame, text="Address Line 2:").grid(row=1, column=0)
address_line2_entry = tk.Entry(address_frame)
address_line2_entry.grid(row=1, column=1)

# Insert Address Button
insert_address_button = tk.Button(address_frame, text="Insert Address", command=insert_address)
insert_address_button.grid(row=2, columnspan=2)

# Address ID for deletion
tk.Label(address_frame, text="Address ID for Deletion:").grid(row=3, column=0)
address_id_entry = tk.Entry(address_frame)
address_id_entry.grid(row=3, column=1)

# Delete Address Button
delete_address_button = tk.Button(address_frame, text="Delete Address", command=delete_address)
delete_address_button.grid(row=4, columnspan=2)

# Create the address table if not exists
create_address_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
