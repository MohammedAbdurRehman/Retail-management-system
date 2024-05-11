import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
try:
    cred_firebase = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred_firebase)
    db_firestore = firestore.client()
except:
    messagebox.showinfo(title="Error", message="Error while connecting to Firebase!")

# Initialize PostgreSQL connection
try:
    conn_postgres = psycopg2.connect(
        dbname="Retail Management System",
        user="postgres",
        password="pgadmin4",
        host="localhost",
        port="5432"
    )
    cur_postgres = conn_postgres.cursor()
except:
    messagebox.showinfo(title="Error", message="Error while connecting to PostgreSQL!")

def create_employee_table_postgres():
    try:
        # Create an employee table in PostgreSQL
        cur_postgres.execute("""
            CREATE TABLE IF NOT EXISTS Employee (
                EmployeeID VARCHAR(50) PRIMARY KEY,
                EmpFirst_Name VARCHAR(50),
                EmpLast_SSN VARCHAR(100),
                EmpMail_Address VARCHAR(100),
                Designation VARCHAR(50),
                Department VARCHAR(50),
                Salary DECIMAL(10, 2),
                Employee_Type VARCHAR(20)
            )
        """)
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Employee table created successfully")
    except Exception as e:
        messagebox.showerror(title="PostgreSQL Error", message=f"Error creating employee table: {e}")

def insert_employee_postgres():
    try:
        # Insert data into the employee table in PostgreSQL
        emp_id = emp_id_entry.get()
        emp_first_name = emp_first_name_entry.get()
        emp_last_ssn = emp_last_ssn_entry.get()
        emp_mail_address = emp_mail_address_entry.get()
        designation = designation_entry.get()
        department = department_var.get()
        salary = salary_entry.get()
        employee_type = employee_type_var.get()

        cur_postgres.execute("""
            INSERT INTO Employee (EmployeeID, EmpFirst_Name, EmpLast_SSN, EmpMail_Address, Designation, Department, Salary, Employee_Type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (emp_id, emp_first_name, emp_last_ssn, emp_mail_address, designation, department, salary, employee_type))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Employee data inserted successfully")
    except Exception as e:
        messagebox.showerror(title="PostgreSQL Error", message=f"Error inserting employee data: {e}")

def delete_employee_postgres():
    try:
        # Delete employee from the employee table in PostgreSQL
        emp_id = delete_emp_id_entry.get()
        cur_postgres.execute("DELETE FROM Employee WHERE EmployeeID = %s", (emp_id,))
        conn_postgres.commit()
        messagebox.showinfo(title="Success", message="PostgreSQL Employee deleted successfully")
    except Exception as e:
        messagebox.showerror(title="PostgreSQL Error", message=f"Error deleting employee: {e}")

def view_employees_postgres():
    try:
        cur_postgres.execute("SELECT * FROM Employee")
        rows = cur_postgres.fetchall()
        if rows:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Employee Records (PostgreSQL)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Employee ID", "First Name", "Last SSN", "Mail Address", "Designation", "Department", "Salary", "Employee Type"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Employee ID")
            tree.heading("#2", text="First Name")
            tree.heading("#3", text="Last SSN")
            tree.heading("#4", text="Mail Address")
            tree.heading("#5", text="Designation")
            tree.heading("#6", text="Department")
            tree.heading("#7", text="Salary")
            tree.heading("#8", text="Employee Type")

            for i, row in enumerate(rows):
                tree.insert("", tk.END, text=str(i+1), values=row)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Employee Records", message="No employee records found in PostgreSQL")
    except psycopg2.Error as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from PostgreSQL: {e}")

def view_employees_firestore():
    try:
        docs = db_firestore.collection('employees').stream()
        if docs:
            # Create a new window for displaying the table
            view_window = tk.Toplevel(window)
            view_window.title("Employee Records (Firebase)")

            # Create Treeview widget for displaying data in tabular form
            tree = ttk.Treeview(view_window, columns=("Employee ID", "First Name", "Last SSN", "Mail Address", "Designation", "Department", "Salary", "Employee Type"))
            tree.heading("#0", text="Index")
            tree.heading("#1", text="Employee ID")
            tree.heading("#2", text="First Name")
            tree.heading("#3", text="Last SSN")
            tree.heading("#4", text="Mail Address")
            tree.heading("#5", text="Designation")
            tree.heading("#6", text="Department")
            tree.heading("#7", text="Salary")
            tree.heading("#8", text="Employee Type")

            for i, doc in enumerate(docs):
                employee_data = doc.to_dict()
                employee_values = (
                    doc.id,
                    employee_data['EmpFirst_Name'],
                    employee_data['EmpLast_SSN'],
                    employee_data['EmpMail_Address'],
                    employee_data['Designation'],
                    employee_data['Department'],
                    employee_data['Salary'],
                    employee_data['Employee_Type']
                )
                tree.insert("", tk.END, text=str(i+1), values=employee_values)

            tree.pack(expand=True, fill="both")
        else:
            messagebox.showinfo(title="Employee Records", message="No employee records found in Firebase")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error viewing data from Firebase: {e}")


def insert_employee_firestore():
    try:
        # Insert data into the employee collection in Firebase
        emp_id = emp_id_entry.get()
        emp_first_name = emp_first_name_entry.get()
        emp_last_ssn = emp_last_ssn_entry.get()
        emp_mail_address = emp_mail_address_entry.get()
        designation = designation_entry.get()
        department = department_var.get()
        salary = salary_entry.get()
        employee_type = employee_type_var.get()

        data = {
            'EmpFirst_Name': emp_first_name,
            'EmpLast_SSN': emp_last_ssn,
            'EmpMail_Address': emp_mail_address,
            'Designation': designation,
            'Department': department,
            'Salary': salary,
            'Employee_Type': employee_type
        }

        db_firestore.collection('employees').document(emp_id).set(data)
        messagebox.showinfo(title="Success", message="Firebase Employee data inserted successfully")
    except Exception as e:
        messagebox.showerror(title="Firebase Error", message=f"Error inserting employee data: {e}")

def delete_employee_firestore():
    try:
        # Delete employee from the employee collection in Firebase
        emp_id = delete_emp_id_entry.get()
        db_firestore.collection('employees').document(emp_id).delete()
        messagebox.showinfo(title="Success", message="Firebase Employee deleted successfully")
    except Exception as e:
        messagebox.showerror(title="Firebase Error", message=f"Error deleting employee: {e}")


# Create the main window
window = tk.Tk()
window.title("Employee Management")

# Create employee management frame
employee_frame = tk.Frame(window)
employee_frame.pack(padx=20, pady=20)

# Employee ID
tk.Label(employee_frame, text="Employee ID:").grid(row=0, column=0)
emp_id_entry = tk.Entry(employee_frame)
emp_id_entry.grid(row=0, column=1)

# First Name
tk.Label(employee_frame, text="First Name:").grid(row=1, column=0)
emp_first_name_entry = tk.Entry(employee_frame)
emp_first_name_entry.grid(row=1, column=1)

# Last SSN
tk.Label(employee_frame, text="Last Name:").grid(row=2, column=0)
emp_last_ssn_entry = tk.Entry(employee_frame)
emp_last_ssn_entry.grid(row=2, column=1)

# Mail Address
tk.Label(employee_frame, text="Mail Address:").grid(row=3, column=0)
emp_mail_address_entry = tk.Entry(employee_frame)
emp_mail_address_entry.grid(row=3, column=1)

# Designation
tk.Label(employee_frame, text="Designation:").grid(row=4, column=0)
designation_entry = tk.Entry(employee_frame)
designation_entry.grid(row=4, column=1)

# Department
tk.Label(employee_frame, text="Department:").grid(row=5, column=0)
departments = ['Sales', 'Marketing', 'HR', 'Management']
department_var = tk.StringVar(value=departments[0])
department_dropdown = ttk.Combobox(employee_frame, textvariable=department_var, values=departments)
department_dropdown.grid(row=5, column=1)

# Salary
tk.Label(employee_frame, text="Salary:").grid(row=6, column=0)
salary_entry = tk.Entry(employee_frame)
salary_entry.grid(row=6, column=1)

# Employee Type
tk.Label(employee_frame, text="Employee Type:").grid(row=7, column=0)
employee_types = ['Permanent', 'Contract']
employee_type_var = tk.StringVar(value=employee_types[0])
employee_type_dropdown = ttk.Combobox(employee_frame, textvariable=employee_type_var, values=employee_types)
employee_type_dropdown.grid(row=7, column=1)

def perform_operations():
    # Insert data into PostgreSQL and Firebase
    insert_employee_postgres()
    insert_employee_firestore()

def delete_data():
    # Delete data from PostgreSQL and Firebase
    delete_employee_postgres()
    delete_employee_firestore()

def view_data():
    # View data from PostgreSQL and Firebase
    view_employees_postgres()
    view_employees_firestore()

# Perform Operations Button
perform_operations_button = tk.Button(employee_frame, text="Insert Employee", command=perform_operations)
perform_operations_button.grid(row=8, column=0)

# Delete Employee Button
delete_employee_button = tk.Button(employee_frame, text="Delete Employee", command=delete_data)
delete_employee_button.grid(row=8, column=1)

# View Employees Button
view_employees_button = tk.Button(employee_frame, text="View Employees", command=view_data)
view_employees_button.grid(row=8, column=2)

# Create the employee table if not exists in PostgreSQL
create_employee_table_postgres()

# Run the main loop
window.mainloop()

# Close PostgreSQL database connection
cur_postgres.close()
conn_postgres.close()
