import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
try:
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except Exception as e:
    messagebox.showerror(title="Error", message=f"Firebase initialization error: {e}")

# Connect to your PostgreSQL database
try:
    conn_postgres = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur_postgres = conn_postgres.cursor()
except psycopg2.Error as e:
    messagebox.showerror(title="Error", message=f"PostgreSQL connection error: {e}")

def create_zip_code_table_postgres():
    try:
        # Create a zip code table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS Zip_Code (
                ZipCode VARCHAR(10) PRIMARY KEY,
                City VARCHAR(50),
                State VARCHAR(50)
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Zip_Code table created successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error creating Zip_Code table: {e}")

def insert_zip_code_postgres():
    try:
        # Insert data into the zip code table in PostgreSQL
        zipcode = zipcode_entry.get()
        city = city_entry.get()
        state = state_entry.get()
        cur_postgres.execute("INSERT INTO Zip_Code(ZipCode, City, State) VALUES (%s, %s, %s)",
                    (zipcode, city, state))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Zip code data inserted successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error inserting Zip code data: {e}")

def delete_zip_code_postgres():
    try:
        # Delete zip code from the zip code table in PostgreSQL
        zipcode = delete_zipcode_entry.get()
        cur_postgres.execute("DELETE FROM Zip_Code WHERE ZipCode = %s", (zipcode,))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Zip code deleted successfully")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error deleting Zip code data: {e}")

def view_zip_codes_postgres():
    try:
        cur_postgres.execute("SELECT * FROM Zip_Code")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Zip Code Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Zip Code", "City", "State"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Zip Code")
            tree.heading("#2", text="City")
            tree.heading("#3", text="State")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Zip Code Records", message="No zip code records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def insert_zip_code_firestore():
    try:
        # Insert data into the zip code collection in Firebase
        zipcode = zipcode_entry.get()
        city = city_entry.get()
        state = state_entry.get()
        data = {'City': city, 'State': state}
        db_firestore.collection('zip_codes').document(zipcode).set(data)
        messagebox.showinfo(title="Success", message="Firebase Zip code data inserted successfully")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error inserting Zip code data to Firebase: {e}")

def delete_zip_code_firestore():
    try:
        # Delete zip code from the zip code collection in Firebase
        zipcode = delete_zipcode_entry.get()
        db_firestore.collection('zip_codes').document(zipcode).delete()
        messagebox.showinfo(title="Success", message="Firebase Zip code deleted successfully")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error deleting Zip code data from Firebase: {e}")

def view_zip_codes_firestore():
    try:
        docs = db_firestore.collection('zip_codes').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Zip Code Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Zip Code", "City", "State"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Zip Code")
            tree.heading("#2", text="City")
            tree.heading("#3", text="State")

            for i, doc in enumerate(docs):
                zip_data = doc.to_dict()
                zip_values = (
                    doc.id,
                    zip_data['City'],
                    zip_data['State']
                )
                tree.insert("", tk.END, text=str(i+1), values=zip_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Zip Code Records", message="No zip code records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")

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

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_zip_code_postgres()
    insert_zip_code_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_zip_code_postgres()
    delete_zip_code_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_zip_codes_postgres()
    view_zip_codes_firestore()

# Insert/Delete/View Zip Code Button
manage_zip_code_button = tk.Button(zip_code_frame, text="Insert Zipcode", command=perform_operations)
manage_zip_code_button.grid(row=3, column=0)

# Delete Zip Code Button
delete_zip_code_button = tk.Button(zip_code_frame, text="Delete Zip Code", command=delete_data)
delete_zip_code_button.grid(row=3, column=1)

# View Zip Codes Button
view_zip_codes_button = tk.Button(zip_code_frame, text="View Zip Codes", command=view_data)
view_zip_codes_button.grid(row=3, column=2)

# Create the zip code table if not exists in PostgreSQL
create_zip_code_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
