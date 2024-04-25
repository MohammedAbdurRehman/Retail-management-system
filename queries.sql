--Stored Procedures:
--Create Stored Procedure to Get Employee by ID:


CREATE OR REPLACE FUNCTION get_employee_by_id(emp_id INT)
RETURNS TABLE(EmployeeID INT, EmpFirst_Name VARCHAR(50), EmpLast_SSN VARCHAR(20), EmpMail_Address VARCHAR(100), Designation VARCHAR(50), Department VARCHAR(50), Salary DECIMAL(10, 2), Employee_Type VARCHAR(20))
AS $$
BEGIN
    RETURN QUERY SELECT * FROM Employee WHERE EmployeeID = emp_id;
END;
$$ LANGUAGE plpgsql;


--Create Stored Procedure to Get Customer by ID:


CREATE OR REPLACE FUNCTION get_customer_by_id(cust_id INT)
RETURNS TABLE(CustomerID INT, First_Name VARCHAR(50), Last_Name VARCHAR(50), Mail_Address VARCHAR(100), Phone_Number VARCHAR(20), Category VARCHAR(50))
AS $$
BEGIN
    RETURN QUERY SELECT * FROM Customer WHERE CustomerID = cust_id;
END;
$$ LANGUAGE plpgsql;
--Triggers:

--Create Trigger to Update Product Availability on Order:

CREATE OR REPLACE FUNCTION update_product_availability()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Product
    SET Available_Number = Available_Number - NEW.Quantity
    WHERE ProductID = NEW.Product_ID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_product_availability_trigger
AFTER INSERT ON Order_Item
FOR EACH ROW
EXECUTE FUNCTION update_product_availability();

--Create Trigger to Calculate Review Score on Review Insertion:


CREATE OR REPLACE FUNCTION calculate_review_score()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Product
    SET Average_Review_Score = (SELECT AVG(Quality) FROM Review WHERE Product_ID = NEW.Product_ID)
    WHERE ProductID = NEW.Product_ID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_review_score_trigger
AFTER INSERT ON Review
FOR EACH ROW
EXECUTE FUNCTION calculate_review_score();
--Views:
--Create View to Get Order Details with Customer Information:


CREATE OR REPLACE VIEW Order_Details AS
SELECT o.Order_ID, o.Shippment_Duration, o.Order_Date, o.Status, c.CustomerID, c.First_Name, c.Last_Name
FROM Orders o
INNER JOIN Customer c ON o.Customer_ID = c.CustomerID;

--Create View to Get Product Reviews:


CREATE OR REPLACE VIEW Product_Reviews AS
SELECT p.ProductID, p.Product_Name, r.Review_ID, r.Quality, r.Defect_Percentage, r.Review_Date
FROM Product p 
INNER JOIN Review r ON p.ProductID = r.Product_ID;