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

def create_product_group_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Product_Group (
            Group_ID SERIAL PRIMARY KEY,
            Group_Name VARCHAR(50)
        )
    """)
    conn.commit()
    messagebox.showinfo(title="Success", message="Product Group table created successfully")

def insert_product_group():
    group_name = group_name_entry.get()
    cur.execute("INSERT INTO Product_Group(Group_Name) VALUES (%s)",
                (group_name,))
    conn.commit()
    messagebox.showinfo(title="Success", message="Product group inserted successfully")

def delete_product_group():
    group_id = group_id_entry.get()
    cur.execute("DELETE FROM Product_Group WHERE Group_ID = %s", (group_id,))
    conn.commit()
    messagebox.showinfo(title="Success", message="Product group deleted successfully")

def view_product_groups():
    cur.execute("SELECT * FROM Product_Group")
    rows = cur.fetchall()
    if rows:
        product_group_records = ""
        for row in rows:
            product_group_records += f"Group ID: {row[0]}, Group Name: {row[1]}\n"
        messagebox.showinfo(title="Product Group Records", message=product_group_records)
    else:
        messagebox.showinfo(title="Product Group Records", message="No product group records found")

# Create the main window
window = tk.Tk()
window.title("Product Group Management")

# Create product group management frame
product_group_frame = tk.Frame(window)
product_group_frame.pack(padx=20, pady=20)

# Group Name
tk.Label(product_group_frame, text="Group Name:").grid(row=0, column=0)
group_name_entry = tk.Entry(product_group_frame)
group_name_entry.grid(row=0, column=1)

# Insert Product Group Button
insert_product_group_button = tk.Button(product_group_frame, text="Insert Product Group", command=insert_product_group)
insert_product_group_button.grid(row=1, column=0)

# Group ID for deletion
tk.Label(product_group_frame, text="Group ID for Deletion:").grid(row=2, column=0)
group_id_entry = tk.Entry(product_group_frame)
group_id_entry.grid(row=2, column=1)

# Delete Product Group Button
delete_product_group_button = tk.Button(product_group_frame, text="Delete Product Group", command=delete_product_group)
delete_product_group_button.grid(row=3, column=0)

# View Product Groups Button
view_product_groups_button = tk.Button(product_group_frame, text="View Product Groups", command=view_product_groups)
view_product_groups_button.grid(row=4, column=0)

# Create the product group table if not exists
create_product_group_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
