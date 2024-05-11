import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
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
window.title("Retail Management System")  # Added title here
window.geometry("800x600")  # Set window size

# Load the JPG image and convert it to a compatible format
jpg_image = Image.open("Types-of-Retail-Stores-2.jpg")  # Replace "path_to_your_image.jpg" with your JPG image path
bg_image = ImageTk.PhotoImage(jpg_image)

# Create a canvas for the background image
canvas = tk.Canvas(window, width=bg_image.width(), height=bg_image.height())
canvas.pack(fill="both", expand=True)

# Set the background image
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Create a frame for the question and table selection buttons
question_frame = ttk.Frame(canvas, padding=20, borderwidth=2, relief="groove")
question_frame.pack(pady=20)

# Question label
question_label = ttk.Label(question_frame, text="Select Table To Perform Operations:", font=("Arial", 16), background="white")
question_label.pack()

# Create a frame for table selection buttons
table_frame = ttk.Frame(canvas, padding=20, borderwidth=2, relief="groove")
table_frame.pack()

# List of table names
tables = [
    "Employee",
    "Customer",
    "Address",
    "ZipCode",
    "Bill",
    "Order",
    "Order Item",
    "Order Product",
    "Product",
    "Voucher",
    "Product Group",
    "Product Description",
    "Review",
    "Payment"
]

# Function to handle button click for each table
def table_button_click(table_name):
    run_table_file(table_name)

# Create styled buttons for each table
for i, table in enumerate(tables):
    table_button = ttk.Button(table_frame, text=table, command=lambda t=table: table_button_click(t), width=20, style="Table.TButton")
    table_button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

# Style for the table buttons
style = ttk.Style()
style.configure("Table.TButton",
                font=("Arial", 14, "bold"),
                foreground="white",
                background="#3498db",
                borderwidth=0,
                highlightthickness=0,
                padx=20,
                pady=10)

# Hover effect for buttons
style.map("Table.TButton",
          foreground=[("active", "white")],
          background=[("active", "#2980b9")])

# Create a label for "A Product By" text
product_by_label = ttk.Label(canvas, text="A Product By:\nAyesha Kashif - 2022132\nMohammad Abdur Rehman - 2022299", font=("Arial", 10), background="white")
product_by_label.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

# Run the main loop
window.mainloop()
