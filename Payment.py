import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize PostgreSQL connection
conn_postgres = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)
cur_postgres = conn_postgres.cursor()

# Initialize Firebase Admin
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()

def create_payment_table_postgres():
    cur_postgres.execute("""
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
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Payment table created successfully")

def insert_payment_postgres():
    payment_type = payment_type_entry.get()
    creditcard_number = creditcard_number_entry.get()
    card_type = card_type_entry.get()
    cvv_number = cvv_number_entry.get()
    expirydate = expirydate_entry.get()
    cardholder_name = cardholder_name_entry.get()
    cur_postgres.execute("INSERT INTO payment(payment_type, creditcard_number, card_type, cvv_number, expirydate, cardholder_name) VALUES (%s, %s, %s, %s, %s, %s)",
                (payment_type, creditcard_number, card_type, cvv_number, expirydate, cardholder_name))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Payment data inserted successfully")

def delete_payment_postgres():
    payment_id = payment_id_entry.get()
    cur_postgres.execute("DELETE FROM payment WHERE payment_id = %s", (payment_id,))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Payment deleted successfully")

def view_payments_postgres():
    cur_postgres.execute("SELECT * FROM payment")
    rows = cur_postgres.fetchall()
    if rows:
        payment_records = ""
        for row in rows:
            payment_records += f"Payment ID: {row[0]}, Type: {row[1]}, Card Number: {row[2]}, Card Type: {row[3]}, CVV: {row[4]}, Expiry Date: {row[5]}, Cardholder: {row[6]}\n"
        messagebox.showinfo(title="Payment Records", message=payment_records)
    else:
        messagebox.showinfo(title="Payment Records", message="No payment records found in PostgreSQL")

def insert_payment_firestore():
    payment_type = payment_type_entry.get()
    creditcard_number = creditcard_number_entry.get()
    card_type = card_type_entry.get()
    cvv_number = cvv_number_entry.get()
    expirydate = expirydate_entry.get()
    cardholder_name = cardholder_name_entry.get()

    data = {
        'payment_type': payment_type,
        'creditcard_number': creditcard_number,
        'card_type': card_type,
        'cvv_number': cvv_number,
        'expirydate': expirydate,
        'cardholder_name': cardholder_name
    }

    doc_ref = db_firestore.collection('payment').add(data)
    messagebox.showinfo(title="Success", message="Firebase Payment data inserted successfully")

def delete_payment_firestore():
    payment_id = payment_id_entry.get()
    db_firestore.collection('payment').document(payment_id).delete()
    messagebox.showinfo(title="Success", message="Firebase Payment deleted successfully")

def view_payments_firestore():
    docs = db_firestore.collection('payment').stream()
    payment_records = ""
    for doc in docs:
        payment_data = doc.to_dict()
        payment_records += f"Payment ID: {doc.id}, Type: {payment_data['payment_type']}, Card Number: {payment_data['creditcard_number']}, Card Type: {payment_data['card_type']}, CVV: {payment_data['cvv_number']}, Expiry Date: {payment_data['expirydate']}, Cardholder: {payment_data['cardholder_name']}\n"
    if payment_records:
        messagebox.showinfo(title="Payment Records", message=payment_records)
    else:
        messagebox.showinfo(title="Payment Records", message="No payment records found in Firebase")

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

def perform_operations():
    # Insert data into PostgreSQL
    insert_payment_postgres()

    # Insert data into Firebase
    insert_payment_firestore()

def delete_data():
    # Delete data from PostgreSQL
    delete_payment_postgres()

    # Delete data from Firebase
    delete_payment_firestore()

def view_data():
    # View data from PostgreSQL
    view_payments_postgres()

    # View data from Firebase
    view_payments_firestore()

# Insert/Delete/View Payment Button
manage_payment_button = tk.Button(payment_frame, text="Perform Operations", command=perform_operations)
manage_payment_button.grid(row=6, column=0)

# Delete Payment Button
delete_payment_button = tk.Button(payment_frame, text="Delete Payment", command=delete_data)
delete_payment_button.grid(row=6, column=1)

# View Payments Button
view_payments_button = tk.Button(payment_frame, text="View Payments", command=view_data)
view_payments_button.grid(row=6, column=2)

# Create the payment table if not exists in PostgreSQL
create_payment_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
