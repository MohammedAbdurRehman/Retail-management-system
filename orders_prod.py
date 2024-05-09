import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()

# Connect to your PostgreSQL database
conn_postgres = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="ayesha",
    host="localhost",
    port="5432"
)
cur_postgres = conn_postgres.cursor()

def create_order_product_table_postgres():
    # Create an order_product table in PostgreSQL
    cur_postgres.execute("""
        CREATE TABLE IF NOT EXISTS Order_Product (
            OrderProduct_ID VARCHAR(100) PRIMARY KEY,
            Order_ID VARCHAR(100) REFERENCES Orders(Order_ID),
            Product_ID VARCHAR(100) REFERENCES Product(ProductID),
            Quantity INT
        )
    """)
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Order_Product table created successfully")

def insert_order_product_postgres():
    # Insert data into the order_product table in PostgreSQL
    order_product_id = order_product_id_entry.get()
    order_id = order_id_entry.get()
    product_id = product_id_entry.get()
    quantity = quantity_entry.get()
    cur_postgres.execute("INSERT INTO Order_Product(OrderProduct_ID, Order_ID, Product_ID, Quantity) VALUES (%s, %s, %s, %s)",
                (order_product_id, order_id, product_id, quantity))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Order_Product data inserted successfully")

def delete_order_product_postgres():
    # Delete order_product from the order_product table in PostgreSQL
    order_product_id = order_product_id_entry.get()
    cur_postgres.execute("DELETE FROM Order_Product WHERE OrderProduct_ID = %s", (order_product_id,))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Order_Product deleted successfully")

def view_order_products_postgres():
    # View order_products from the order_product table in PostgreSQL
    cur_postgres.execute("SELECT * FROM Order_Product")
    rows = cur_postgres.fetchall()
    if rows:
        order_product_records = ""
        for row in rows:
            order_product_records += f"OrderProduct ID: {row[0]}, Order ID: {row[1]}, Product ID: {row[2]}, Quantity: {row[3]}\n"
        messagebox.showinfo(title="Order_Product Records (PostgreSQL)", message=order_product_records)
    else:
        messagebox.showinfo(title="Order_Product Records (PostgreSQL)", message="No order product records found")

def insert_order_product_firestore():
    # Insert data into the order_product collection in Firebase
    order_product_id = order_product_id_entry.get()
    order_id = order_id_entry.get()
    product_id = product_id_entry.get()
    quantity = quantity_entry.get()

    data = {
        'Order_ID': order_id,
        'Product_ID': product_id,
        'Quantity': int(quantity)
    }

    db_firestore.collection('order_products').document(order_product_id).set(data)
    messagebox.showinfo(title="Success", message="Firebase Order_Product data inserted successfully")

def delete_order_product_firestore():
    # Delete order_product from the order_product collection in Firebase
    order_product_id = order_product_id_entry.get()
    db_firestore.collection('order_products').document(order_product_id).delete()
    messagebox.showinfo(title="Success", message="Firebase Order_Product deleted successfully")

def view_order_products_firestore():
    # View order_products from the order_product collection in Firebase
    docs = db_firestore.collection('order_products').stream()
    order_product_records = ""
    for doc in docs:
        order_product_data = doc.to_dict()
        order_product_records += f"OrderProduct ID: {doc.id}, Order ID: {order_product_data['Order_ID']}, Product ID: {order_product_data['Product_ID']}, Quantity: {order_product_data['Quantity']}\n"
    if order_product_records:
        messagebox.showinfo(title="Order_Product Records (Firebase)", message=order_product_records)
    else:
        messagebox.showinfo(title="Order_Product Records (Firebase)", message="No order product records found in Firebase")

# Create the main window
window = tk.Tk()
window.title("Order Product Management")

# Create order product management frame
order_product_frame = tk.Frame(window)
order_product_frame.pack(padx=20, pady=20)

# OrderProduct ID
tk.Label(order_product_frame, text="OrderProduct ID:").grid(row=0, column=0)
order_product_id_entry = tk.Entry(order_product_frame)
order_product_id_entry.grid(row=0, column=1)

# Order ID
tk.Label(order_product_frame, text="Order ID:").grid(row=1, column=0)
order_id_entry = tk.Entry(order_product_frame)
order_id_entry.grid(row=1, column=1)

# Product ID
tk.Label(order_product_frame, text="Product ID:").grid(row=2, column=0)
product_id_entry = tk.Entry(order_product_frame)
product_id_entry.grid(row=2, column=1)

# Quantity
tk.Label(order_product_frame, text="Quantity:").grid(row=3, column=0)
quantity_entry = tk.Entry(order_product_frame)
quantity_entry.grid(row=3, column=1)

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_order_product_postgres()
    insert_order_product_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_order_product_postgres()
    delete_order_product_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_order_products_postgres()
    view_order_products_firestore()

# Perform Operations Button
perform_operations_button = tk.Button(order_product_frame, text="Perform Operations", command=perform_operations)
perform_operations_button.grid(row=4, column=0)

# Delete Order Product Button
delete_order_product_button = tk.Button(order_product_frame, text="Delete Order Product", command=delete_data)
delete_order_product_button.grid(row=4, column=1)

# View Order Products Button
view_order_products_button = tk.Button(order_product_frame, text="View Order Products", command=view_data)
view_order_products_button.grid(row=4, column=2)

# Create the order product table if not exists in PostgreSQL
create_order_product_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
