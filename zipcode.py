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

def create_zip_code_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Zip_Code (
            ZipCode VARCHAR(10) PRIMARY KEY,
            City VARCHAR(50),
            State VARCHAR(50)
        )
    """)
    conn.commit()
    messagebox.showinfo(title="Success", message="Zip_Code table created successfully")

def insert_zip_code():
    zipcode = zipcode_entry.get()
    city = city_entry.get()
    state = state_entry.get()
    cur.execute("INSERT INTO Zip_Code(ZipCode, City, State) VALUES (%s, %s, %s)",
                (zipcode, city, state))
    conn.commit()
    messagebox.showinfo(title="Success", message="Zip code data inserted successfully")

def delete_zip_code():
    zipcode = zipcode_entry.get()
    cur.execute("DELETE FROM Zip_Code WHERE ZipCode = %s", (zipcode,))
    conn.commit()
    messagebox.showinfo(title="Success", message="Zip code deleted successfully")

def view_zip_codes():
    cur.execute("SELECT * FROM Zip_Code")
    rows = cur.fetchall()
    if rows:
        zip_code_records = ""
        for row in rows:
            zip_code_records += f"Zip Code: {row[0]}, City: {row[1]}, State: {row[2]}\n"
        messagebox.showinfo(title="Zip Code Records", message=zip_code_records)
    else:
        messagebox.showinfo(title="Zip Code Records", message="No zip code records found")

# Create the main window
window = tk.Tk()
window.title("Zip Code Management")

# Create zip code management frame
zip_code_frame = tk.Frame(window)
zip_code_frame.pack(padx=20, pady=20)

# Zip Code
tk.Label(zip_code_frame, text="Zip Code:").grid(row=0, column=0)
zipcode_entry = tk.Entry(zip_code_frame)
zipcode_entry.grid(row=0, column=1)

# City
tk.Label(zip_code_frame, text="City:").grid(row=1, column=0)
city_entry = tk.Entry(zip_code_frame)
city_entry.grid(row=1, column=1)

# State
tk.Label(zip_code_frame, text="State:").grid(row=2, column=0)
state_entry = tk.Entry(zip_code_frame)
state_entry.grid(row=2, column=1)

# Insert Zip Code Button
insert_zip_code_button = tk.Button(zip_code_frame, text="Insert Zip Code", command=insert_zip_code)
insert_zip_code_button.grid(row=3, column=0)

# Zip Code for deletion
tk.Label(zip_code_frame, text="Zip Code for Deletion:").grid(row=4, column=0)
delete_zipcode_entry = tk.Entry(zip_code_frame)
delete_zipcode_entry.grid(row=4, column=1)

# Delete Zip Code Button
delete_zip_code_button = tk.Button(zip_code_frame, text="Delete Zip Code", command=delete_zip_code)
delete_zip_code_button.grid(row=5, column=0)

# View Zip Codes Button
view_zip_codes_button = tk.Button(zip_code_frame, text="View Zip Codes", command=view_zip_codes)
view_zip_codes_button.grid(row=6, column=0)

# Create the zip code table if not exists
create_zip_code_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
