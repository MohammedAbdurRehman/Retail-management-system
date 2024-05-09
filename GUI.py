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
window.title("Retail Management System")

# Employee ID
tk.Label(employee_frame, text="Employee ID:").grid(row=0, column=0)
entry_emp_id = tk.Entry(employee_frame)
entry_emp_id.grid(row=0, column=1)

# First Name
tk.Label(employee_frame, text="First Name:").grid(row=1, column=0)
entry_first_name = tk.Entry(employee_frame)
entry_first_name.grid(row=1, column=1)

# Last SSN
tk.Label(employee_frame, text="Last SSN:").grid(row=2, column=0)
entry_last_ssn = tk.Entry(employee_frame)
entry_last_ssn.grid(row=2, column=1)

# Mail Address
tk.Label(employee_frame, text="Mail Address:").grid(row=3, column=0)
entry_mail_address = tk.Entry(employee_frame)
entry_mail_address.grid(row=3, column=1)

# Designation
tk.Label(employee_frame, text="Designation:").grid(row=4, column=0)
entry_designation = tk.Entry(employee_frame)
entry_designation.grid(row=4, column=1)

# Department
tk.Label(employee_frame, text="Department:").grid(row=5, column=0)
entry_department = tk.Entry(employee_frame)
entry_department.grid(row=5, column=1)

# Salary
tk.Label(employee_frame, text="Salary:").grid(row=6, column=0)
entry_salary = tk.Entry(employee_frame)
entry_salary.grid(row=6, column=1)

# Employee Type
tk.Label(employee_frame, text="Employee Type:").grid(row=7, column=0)
entry_employee_type = tk.Entry(employee_frame)
entry_employee_type.grid(row=7, column=1)

# Buttons for employee management
btn_create_employee = tk.Button(employee_frame, text="Create Employee", command=create_employee)
btn_create_employee.grid(row=8, column=0)

btn_read_employee = tk.Button(employee_frame, text="Read Employee", command=read_employee)
btn_read_employee.grid(row=8, column=1)

btn_delete_employee = tk.Button(employee_frame, text="Delete Employee", command=delete_employee)
btn_delete_employee.grid(row=8, column=2)

# Run the main loop
window.mainloop()

# Close the database connection
cur.close()
conn.close()
