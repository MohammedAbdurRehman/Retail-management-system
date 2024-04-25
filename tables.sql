-- Create Employee table
CREATE TABLE Employee (
    EmployeeID varchar(50) PRIMARY KEY,
    EmpFirst_Name VARCHAR(50),
    EmpLast_SSN VARCHAR(100),
    EmpMail_Address VARCHAR(100),
    Designation VARCHAR(50),
    Department VARCHAR(50),
    Salary DECIMAL(10, 2),
    Employee_Type VARCHAR(20)
);

CREATE TABLE Customer (
    CustomerID SERIAL PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Mail_Address VARCHAR(100),
    Phone_Number VARCHAR(20),
    Category VARCHAR(50)
);

CREATE TABLE Address (
	CustomerID SERIAL REFERENCES Customer(CustomerID),
    AddressID VARCHAR(50) PRIMARY KEY,
    Address_line1 VARCHAR(100),
    Address_line2 TEXT
);

-- Create Zip Code table
CREATE TABLE Zip_Code (
    ZipCode VARCHAR(10) PRIMARY KEY,
    City VARCHAR(50),
    State VARCHAR(50)
);

-- Create Bill table
CREATE TABLE Bill (
    Billing_ID varchar(50) PRIMARY KEY,
    Amount_Paid DECIMAL(10, 2)
);

-- Create Payment table
CREATE TABLE Payment (
    Payment_ID VARCHAR(50) PRIMARY KEY,
    Payment_Type VARCHAR(50),
    CreditCard_Number VARCHAR(100),
    Card_Type VARCHAR(100),
    CVV_Number VARCHAR(50),
    CardHolder_Name VARCHAR(100),
	CustomerID SERIAL REFERENCES Customer(CustomerID)
);

-- Create Orders table
CREATE TABLE Orders (
    Order_ID VARCHAR(100) PRIMARY KEY,
    Shippment_Duration VARCHAR(100),
    Order_Date DATE,
    Status VARCHAR(100)
);

-- Create Order Item table
CREATE TABLE Order_Item (
    OrderItem_ID SERIAL PRIMARY KEY,
    Order_ID INT REFERENCES Orders(Order_ID),
    Date_of_Order DATE,
    Quantity INT
);

-- Create Product table
CREATE TABLE Product (
    ProductID VARCHAR(100) PRIMARY KEY,
    Product_Name VARCHAR(100),
    Available_Number INT,
	
);

-- Create Order Product table
CREATE TABLE Order_Product (
    OrderProduct_ID VARCHAR(100) PRIMARY KEY,
    Order_ID VARCHAR(100) REFERENCES Orders(Order_ID),
    Product_ID VARCHAR(100) REFERENCES Product(ProductID),
    Quantity INT
);

-- Create Voucher table
CREATE TABLE Voucher (
    Voucher_ID VARCHAR(20) PRIMARY KEY,
    Discount_percent INT
);



-- Create Product Details table
CREATE TABLE Product_Details (
    ProductID VARCHAR(50) REFERENCES Product(ProductID) PRIMARY KEY,
    Weight DECIMAL(10, 2),
    Width DECIMAL(10, 2),
    Colour VARCHAR(50),
    Height DECIMAL(10, 2)
);

-- Create Product Group table
CREATE TABLE Product_Group (
    Group_ID SERIAL PRIMARY KEY,
    Group_Name VARCHAR(50)
);

-- Create Review table
CREATE TABLE Review (
    Review_ID VARCHAR(100) PRIMARY KEY,
    Quality INT,
    Defect_Percentage INT,
    ProductID VARCHAR REFERENCES Product(ProductID)
);