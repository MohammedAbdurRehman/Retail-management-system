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
    dbname="Retail Management",
    user="postgres",
    password="ayesha",
    host="localhost",
    port="5432"
)
cur_postgres = conn_postgres.cursor()

def create_employee_table_postgres():
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

def insert_employee_postgres():
    # Insert data into the employee table in PostgreSQL
    emp_id = emp_id_entry.get()
    emp_first_name = emp_first_name_entry.get()
    emp_last_ssn = emp_last_ssn_entry.get()
    emp_mail_address = emp_mail_address_entry.get()
    designation = designation_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    employee_type = employee_type_entry.get()

    cur_postgres.execute("""
        INSERT INTO Employee (EmployeeID, EmpFirst_Name, EmpLast_SSN, EmpMail_Address, Designation, Department, Salary, Employee_Type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (emp_id, emp_first_name, emp_last_ssn, emp_mail_address, designation, department, salary, employee_type))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Employee data inserted successfully")

def delete_employee_postgres():
    # Delete employee from the employee table in PostgreSQL
    emp_id = delete_emp_id_entry.get()
    cur_postgres.execute("DELETE FROM Employee WHERE EmployeeID = %s", (emp_id,))
    conn_postgres.commit()
    messagebox.showinfo(title="Success", message="PostgreSQL Employee deleted successfully")

def view_employees_postgres():
    # View employees from the employee table in PostgreSQL
    cur_postgres.execute("SELECT * FROM Employee")
    rows = cur_postgres.fetchall()
    if rows:
        employee_records = ""
        for row in rows:
            employee_records += f"Employee ID: {row[0]}, Name: {row[1]} {row[2]}, Mail Address: {row[3]}, Designation: {row[4]}, Department: {row[5]}, Salary: {row[6]}, Employee Type: {row[7]}\n"
        messagebox.showinfo(title="Employee Records (PostgreSQL)", message=employee_records)
    else:
        messagebox.showinfo(title="Employee Records (PostgreSQL)", message="No employee records found")

def insert_employee_firestore():
    # Insert data into the employee collection in Firebase
    emp_id = emp_id_entry.get()
    emp_first_name = emp_first_name_entry.get()
    emp_last_ssn = emp_last_ssn_entry.get()
    emp_mail_address = emp_mail_address_entry.get()
    designation = designation_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    employee_type = employee_type_entry.get()

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

def delete_employee_firestore():
    # Delete employee from the employee collection in Firebase
    emp_id = delete_emp_id_entry.get()
    db_firestore.collection('employees').document(emp_id).delete()
    messagebox.showinfo(title="Success", message="Firebase Employee deleted successfully")

def view_employees_firestore():
    # View employees from the employee collection in Firebase
    docs = db_firestore.collection('employees').stream()
    employee_records = ""
    for doc in docs:
        employee_data = doc.to_dict()
        employee_records += f"Employee ID: {doc.id}, Name: {employee_data['EmpFirst_Name']} {employee_data['EmpLast_SSN']}, Mail Address: {employee_data['EmpMail_Address']}, Designation: {employee_data['Designation']}, Department: {employee_data['Department']}, Salary: {employee_data['Salary']}, Employee Type: {employee_data['Employee_Type']}\n"
    if employee_records:
        messagebox.showinfo(title="Employee Records (Firebase)", message=employee_records)
    else:
        messagebox.showinfo(title="Employee Records (Firebase)", message="No employee records found in Firebase")

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
tk.Label(employee_frame, text="Last SSN:").grid(row=2, column=0)
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
department_entry = tk.Entry(employee_frame)
department_entry.grid(row=5, column=1)

# Salary
tk.Label(employee_frame, text="Salary:").grid(row=6, column=0)
salary_entry = tk.Entry(employee_frame)
salary_entry.grid(row=6, column=1)

# Employee Type
tk.Label(employee_frame, text="Employee Type:").grid(row=7, column=0)
employee_type_entry = tk.Entry(employee_frame)
employee_type_entry.grid(row=7, column=1)

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
