import tkinter as tk
from tkinter import messagebox
import psycopg2

conn = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_payment_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payment (
            payment_id SERIAL PRIMARY KEY,
            payment_type VARCHAR(20),
            creditcard_number VARCHAR(20),
            card_type VARCHAR(20),
            cvv_number VARCHAR(10),
            expirydate DATE,
            cardholder_name VARCHAR(100)
        )
    """)
    conn.commit()
    messagebox.showinfo(title="Success", message="Payment table created successfully")

def insert_payment():
    payment_type = payment_type_entry.get()
    creditcard_number = creditcard_number_entry.get()
    card_type = card_type_entry.get()
    cvv_number = cvv_number_entry.get()
    expirydate = expirydate_entry.get()
    cardholder_name = cardholder_name_entry.get()
    cur.execute("INSERT INTO payment(payment_type, creditcard_number, card_type, cvv_number, expirydate, cardholder_name) VALUES (%s, %s, %s, %s, %s, %s)",
                (payment_type, creditcard_number, card_type, cvv_number, expirydate, cardholder_name))
    conn.commit()
    messagebox.showinfo(title="Success", message="Payment data inserted successfully")

def delete_payment():
    payment_id = payment_id_entry.get()
    cur.execute("DELETE FROM payment WHERE payment_id = %s", (payment_id,))
    conn.commit()
    messagebox.showinfo(title="Success", message="Payment deleted successfully")

def view_payments():
    cur.execute("SELECT * FROM payment")
    rows = cur.fetchall()
    if rows:
        payment_records = ""
        for row in rows:
            payment_records += f"Payment ID: {row[0]}, Type: {row[1]}, Card Number: {row[2]}, Card Type: {row[3]}, CVV: {row[4]}, Expiry Date: {row[5]}, Cardholder: {row[6]}\n"
        messagebox.showinfo(title="Payment Records", message=payment_records)
    else:
        messagebox.showinfo(title="Payment Records", message="No payment records found")

# Create the main window
window = tk.Tk()
window.title("Payment Management")

# Create payment management frame
payment_frame = tk.Frame(window)
payment_frame.pack(padx=20, pady=20)

# Payment Type
tk.Label(payment_frame, text="Payment Type:").grid(row=0, column=0)
payment_type_entry = tk.Entry(payment_frame)
payment_type_entry.grid(row=0, column=1)

# Credit Card Number
tk.Label(payment_frame, text="Credit Card Number:").grid(row=1, column=0)
creditcard_number_entry = tk.Entry(payment_frame)
creditcard_number_entry.grid(row=1, column=1)

# Card Type
tk.Label(payment_frame, text="Card Type:").grid(row=2, column=0)
card_type_entry = tk.Entry(payment_frame)
card_type_entry.grid(row=2, column=1)

# CVV Number
tk.Label(payment_frame, text="CVV Number:").grid(row=3, column=0)
cvv_number_entry = tk.Entry(payment_frame)
cvv_number_entry.grid(row=3, column=1)

# Expiry Date
tk.Label(payment_frame, text="Expiry Date (YYYY-MM-DD):").grid(row=4, column=0)
expirydate_entry = tk.Entry(payment_frame)
expirydate_entry.grid(row=4, column=1)

# Cardholder Name
tk.Label(payment_frame, text="Cardholder Name:").grid(row=5, column=0)
cardholder_name_entry = tk.Entry(payment_frame)
cardholder_name_entry.grid(row=5, column=1)

# Insert Payment Button
insert_payment_button = tk.Button(payment_frame, text="Insert Payment", command=insert_payment)
insert_payment_button.grid(row=6, column=0)

# Payment ID for deletion
tk.Label(payment_frame, text="Payment ID for Deletion:").grid(row=7, column=0)
payment_id_entry = tk.Entry(payment_frame)
payment_id_entry.grid(row=7, column=1)

# Delete Payment Button
delete_payment_button = tk.Button(payment_frame, text="Delete Payment", command=delete_payment)
delete_payment_button.grid(row=8, column=0)

# View Payments Button
view_payments_button = tk.Button(payment_frame, text="View Payments", command=view_payments)
view_payments_button.grid(row=9, column=0)

# Create the payment table if not exists
create_payment_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
