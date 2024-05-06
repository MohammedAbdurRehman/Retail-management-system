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

def create_bill_table():
    # Create a bill table in the database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bill (
            billing_id SERIAL PRIMARY KEY,
            amount_paid NUMERIC(10, 2)
        )
    """)
    conn.commit()
    messagebox.showinfo("Success", "Bill table created successfully")

def insert_bill():
    # Insert data into the bill table
    amount_paid = amount_paid_entry.get()
    cur.execute("INSERT INTO bill (amount_paid) VALUES (%s)", (amount_paid,))
    conn.commit()
    messagebox.showinfo("Success", "Bill data inserted successfully")

def delete_bill():
    # Delete bill from the bill table
    billing_id = billing_id_entry.get()
    cur.execute("DELETE FROM bill WHERE billing_id = %s", (billing_id,))
    conn.commit()
    messagebox.showinfo("Success", "Bill deleted successfully")

# Create the main window
window = tk.Tk()
window.title("Bill Management")

# Create bill management frame
bill_frame = tk.Frame(window)
bill_frame.pack(padx=20, pady=20)

# Amount Paid
tk.Label(bill_frame, text="Amount Paid:").grid(row=0, column=0)
amount_paid_entry = tk.Entry(bill_frame)
amount_paid_entry.grid(row=0, column=1)

# Insert Bill Button
insert_bill_button = tk.Button(bill_frame, text="Insert Bill", command=insert_bill)
insert_bill_button.grid(row=1, columnspan=2)

# Billing ID for deletion
tk.Label(bill_frame, text="Billing ID for Deletion:").grid(row=2, column=0)
billing_id_entry = tk.Entry(bill_frame)
billing_id_entry.grid(row=2, column=1)

# Delete Bill Button
delete_bill_button = tk.Button(bill_frame, text="Delete Bill", command=delete_bill)
delete_bill_button.grid(row=3, columnspan=2)

# Create the bill table if not exists
create_bill_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
