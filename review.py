import tkinter as tk
from tkinter import messagebox
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase
cred_firebase = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred_firebase)
db_firestore = firestore.client()

# Initialize PostgreSQL connection
conn = psycopg2.connect(
    dbname="Retail Management",
    user="postgres",
    password="ayesha",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_review_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Review (
            Review_ID VARCHAR(100) PRIMARY KEY,
            Quality INT,
            Defect_Percentage INT,
            ProductID VARCHAR REFERENCES Product(ProductID)
        )
    """)
    conn.commit()
    messagebox.showinfo(title="Success", message="Review table created successfully")

def insert_review():
    review_id = review_id_entry.get()
    quality = quality_entry.get()
    defect_percentage = defect_percentage_entry.get()
    product_id = product_id_entry.get()
    cur.execute("INSERT INTO Review(Review_ID, Quality, Defect_Percentage, ProductID) VALUES (%s, %s, %s, %s)",
                (review_id, quality, defect_percentage, product_id))
    conn.commit()

    # Firebase
    firebase_db.reference('Review').child(review_id).set({
        'Quality': quality,
        'Defect_Percentage': defect_percentage,
        'ProductID': product_id
    })

    messagebox.showinfo(title="Success", message="Review data inserted successfully")

def delete_review():
    review_id = review_id_entry.get()
    cur.execute("DELETE FROM Review WHERE Review_ID = %s", (review_id,))
    conn.commit()

    # Firebase
    firebase_db.reference('Review').child(review_id).delete()

    messagebox.showinfo(title="Success", message="Review deleted successfully")

def view_reviews():
    cur.execute("SELECT * FROM Review")
    rows = cur.fetchall()
    if rows:
        review_records = ""
        for row in rows:
            review_records += f"Review ID: {row[0]}, Quality: {row[1]}, Defect Percentage: {row[2]}, ProductID: {row[3]}\n"
        messagebox.showinfo(title="Review Records", message=review_records)
    else:
        messagebox.showinfo(title="Review Records", message="No review records found")

# Create the main window
window = tk.Tk()
window.title("Review Management")

# Create review management frame
review_frame = tk.Frame(window)
review_frame.pack(padx=20, pady=20)

# Review ID
tk.Label(review_frame, text="Review ID:").grid(row=0, column=0)
review_id_entry = tk.Entry(review_frame)
review_id_entry.grid(row=0, column=1)

# Quality
tk.Label(review_frame, text="Quality:").grid(row=1, column=0)
quality_entry = tk.Entry(review_frame)
quality_entry.grid(row=1, column=1)

# Defect Percentage
tk.Label(review_frame, text="Defect Percentage:").grid(row=2, column=0)
defect_percentage_entry = tk.Entry(review_frame)
defect_percentage_entry.grid(row=2, column=1)

# Product ID
tk.Label(review_frame, text="Product ID:").grid(row=3, column=0)
product_id_entry = tk.Entry(review_frame)
product_id_entry.grid(row=3, column=1)

# Insert Review Button
insert_review_button = tk.Button(review_frame, text="Insert Review", command=insert_review)
insert_review_button.grid(row=4, column=0)

# Review ID for deletion
tk.Label(review_frame, text="Review ID for Deletion:").grid(row=5, column=0)
review_id_entry = tk.Entry(review_frame)
review_id_entry.grid(row=5, column=1)

# Delete Review Button
delete_review_button = tk.Button(review_frame, text="Delete Review", command=delete_review)
delete_review_button.grid(row=6, column=0)

# View Reviews Button
view_reviews_button = tk.Button(review_frame, text="View Reviews", command=view_reviews)
view_reviews_button.grid(row=7, column=0)

# Create the review table if not exists
create_review_table()

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
