import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

# Function to run the Python file for the selected table
def run_table_file(table_name):
    file_name = f"{table_name.lower().replace(' ', '_')}.py"
    if os.path.exists(file_name):
        os.system(f"python {file_name}")
    else:
        messagebox.showerror("Error", f"Python file for table {table_name} not found!")

# Create the main window
window = tk.Tk()
window.title("Table Selection")

# Create a frame for the question and table selection buttons
question_frame = ttk.Frame(window, padding=20)
question_frame.grid(row=0, column=0, padx=20, pady=20)

# Question label
question_label = ttk.Label(question_frame, text="Select which table you want to insert data into:")
question_label.pack()

# Create a frame for table selection buttons
table_frame = ttk.Frame(window, padding=20)
table_frame.grid(row=1, column=0, padx=20, pady=20)

# List of table names
tables = [
    "Employee",
    "Customer",
    "Address",
    "Zip Code",
    "Bill",
    "Payment Mode",
    "Order",
    "Order Item",
    "Order Product",
    "Product",
    "Voucher",
    "Product Group",
    "Product Description",
    "Reviews"
]

# Function to handle button click for each table
def table_button_click(table_name):
    run_table_file(table_name)

# Create styled buttons for each table
for i, table in enumerate(tables):
    table_button = ttk.Button(table_frame, text=table, command=lambda t=table: table_button_click(t), width=20)
    table_button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

# Run the main loop
window.mainloop()
