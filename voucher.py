import tkinter as tk
from tkinter import messagebox
import psycopg2

conn = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="ayesha",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_voucher_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Voucher (
            Voucher_ID VARCHAR(20) PRIMARY KEY,
            Discount_percent INT
        )
    """)
    conn.commit()
    messagebox.showinfo(title="Success", message="Voucher table created successfully")

def insert_voucher():
    voucher_id = voucher_id_entry.get()
    discount_percent = discount_percent_entry.get()
    cur.execute("INSERT INTO Voucher(Voucher_ID, Discount_percent) VALUES (%s, %s)",
                (voucher_id, discount_percent))
    conn.commit()
    messagebox.showinfo(title="Success", message="Voucher data inserted successfully")

def delete_voucher():
    voucher_id = voucher_id_entry.get()
    cur.execute("DELETE FROM Voucher WHERE Voucher_ID = %s", (voucher_id,))
    conn.commit()
    messagebox.showinfo(title="Success", message="Voucher deleted successfully")

def view_vouchers():
    cur.execute("SELECT * FROM Voucher")
    rows = cur.fetchall()
    if rows:
        voucher_records = ""
        for row in rows:
            voucher_records += f"Voucher ID: {row[0]}, Discount Percent: {row[1]}\n"
        messagebox.showinfo(title="Voucher Records", message=voucher_records)
    else:
        messagebox.showinfo(title="Voucher Records", message="No voucher records found")

# Create the main window
window = tk.Tk()
window.title("Voucher Management")

# Create voucher management frame
voucher_frame = tk.Frame(window)
voucher_frame.pack(padx=20, pady=20)

# Voucher ID
tk.Label(voucher_frame, text="Voucher ID:").grid(row=0, column=0)
voucher_id_entry = tk.Entry(voucher_frame)
voucher_id_entry.grid(row=0, column=1)

# Discount Percent
tk.Label(voucher_frame, text="Discount Percent:").grid(row=1, column=0)
discount_percent_entry = tk.Entry(voucher_frame)
discount_percent_entry.grid(row=1, column=1)

# Insert Voucher Button
insert_voucher_button = tk.Button(voucher_frame, text="Insert Voucher", command=insert_voucher)
insert_voucher_button.grid(row=2, column=0)

# Voucher ID for deletion
tk.Label(voucher_frame, text="Voucher ID for Deletion:").grid(row=3, column=0)
voucher_id_entry = tk.Entry(voucher_frame)
voucher_id_entry.grid(row=3, column=1)

# Delete Voucher Button
delete_voucher_button = tk.Button(voucher_frame, text="Delete Voucher", command=delete_voucher)
delete_voucher_button.grid(row=4, column=0)

# View Vouchers Button
view_vouchers_button = tk.Button(voucher_frame, text="View Vouchers", command=view_vouchers)
view_vouchers_button.grid(row=5, column=0)

# Create the voucher table if not exists
create_voucher_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
