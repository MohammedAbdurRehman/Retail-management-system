import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="Retail Management System",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

def create_employee():
    emp_first_name = entry_first_name.get()
    emp_last_ssn = entry_last_ssn.get()
    emp_mail_address = entry_mail_address.get()
    designation = entry_designation.get()
    department = entry_department.get()
    salary = entry_salary.get()
    employee_type = entry_employee_type.get()

    # Execute SQL INSERT query
    try:
        cur.execute("INSERT INTO Employee (EmpFirst_Name, EmpLast_SSN, EmpMail_Address, Designation, Department, Salary, Employee_Type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (emp_first_name, emp_last_ssn, emp_mail_address, designation, department, salary, employee_type))
        conn.commit()
        messagebox.showinfo("Success", "Employee created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating employee: {str(e)}")

def read_employee():
    emp_id = entry_emp_id.get()
    cur.execute("SELECT * FROM Employee WHERE EmployeeID = %s", (emp_id,))
    employee = cur.fetchone()
    if employee:
        messagebox.showinfo("Employee Details", f"EmployeeID: {employee[0]}\nName: {employee[1]} {employee[2]}\nMail Address: {employee[3]}\nDesignation: {employee[4]}\nDepartment: {employee[5]}\nSalary: {employee[6]}\nEmployee Type: {employee[7]}")
    else:
        messagebox.showerror("Error", "Employee not found!")

def delete_employee():
    emp_id = entry_emp_id.get()
    cur.execute("DELETE FROM Employee WHERE EmployeeID = %s", (emp_id,))
    conn.commit()
    messagebox.showinfo("Success", "Employee deleted successfully!")

# Create the main window
window = tk.Tk()
window.title("Employee Management System")

# Create labels and entry fields
label_emp_id = tk.Label(window, text="Employee ID:")
label_emp_id.grid(row=0, column=0)
entry_emp_id = tk.Entry(window)
entry_emp_id.grid(row=0, column=1)

label_first_name = tk.Label(window, text="First Name:")
label_first_name.grid(row=1, column=0)
entry_first_name = tk.Entry(window)
entry_first_name.grid(row=1, column=1)

label_last_ssn = tk.Label(window, text="Last SSN:")
label_last_ssn.grid(row=2, column=0)
entry_last_ssn = tk.Entry(window)
entry_last_ssn.grid(row=2, column=1)

label_mail_address = tk.Label(window, text="Mail Address:")
label_mail_address.grid(row=3, column=0)
entry_mail_address = tk.Entry(window)
entry_mail_address.grid(row=3, column=1)

label_designation = tk.Label(window, text="Designation:")
label_designation.grid(row=4, column=0)
entry_designation = tk.Entry(window)
entry_designation.grid(row=4, column=1)

label_department = tk.Label(window, text="Department:")
label_department.grid(row=5, column=0)
entry_department = tk.Entry(window)
entry_department.grid(row=5, column=1)

label_salary = tk.Label(window, text="Salary:")
label_salary.grid(row=6, column=0)
entry_salary = tk.Entry(window)
entry_salary.grid(row=6, column=1)

label_employee_type = tk.Label(window, text="Employee Type:")
label_employee_type.grid(row=7, column=0)
entry_employee_type = tk.Entry(window)
entry_employee_type.grid(row=7, column=1)

# Create buttons
btn_create_employee = tk.Button(window, text="Create Employee", command=create_employee)
btn_create_employee.grid(row=8, column=0)

btn_read_employee = tk.Button(window, text="Read Employee", command=read_employee)
btn_read_employee.grid(row=8, column=1)

btn_delete_employee = tk.Button(window, text="Delete Employee", command=delete_employee)
btn_delete_employee.grid(row=8, column=2)

# Run the main loop
window.mainloop()
