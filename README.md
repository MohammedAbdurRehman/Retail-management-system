# Retail Management System

## Entities:
* Employee
* Customer
* Address
* Zipcode
* Bill
* Product
* Product_Description
* Orders
* Order Product
* Product Group
* Order Item
* Voucher 
* Review

## ERD and Project Schema:
![image](https://github.com/MohammedAbdurRehman/Retail-management-system/blob/main/ERD.png)

![image](https://github.com/MohammedAbdurRehman/Retail-management-system/blob/main/Schema.png)

## Semantic Object Model Diagram:
![image](https://github.com/MohammedAbdurRehman/Retail-management-system/assets/162794845/2283b502-3ec5-4084-9def-6cc5700658e7)

## Database Project Architecture Diagram:

## Project Description:

* ### Main Interface
The project can be navigated by running main.py file in the repository, Interface of main.py is given below:
<img width="794" alt="Main" src="https://github.com/MohammedAbdurRehman/Retail-management-system/assets/162794845/63c739b6-3a6f-46fc-bc52-5c574a6984fd">
* ### Employee
  This function is used to insert, delete and view employee data that includes:
  * Employee id
  * First name
  * Last name
  * Designation
  * Department
  * Salary
  * Type
* ### Customer
  This function is used to insert, delete and view Customer data that includes:
  * Customer Id
  * First name
  * Last name
  * mail address
  * Phone
  * Category
* ### Address
  This function is used to insert, delete and view address that includes
  * Address line 1
  * Address line 2
* ### Order
  This function is used to insert and delete order
  * Shipment Duration
  * Order Date
  * Status
* ### Order Item
  Used to insert, delete and view:
  * Order id
  * Date of order
  * Quantity
* ### Order Product
  Used to insert, delete and view
  * Order product ID
  * Order ID
  * Product ID
  * Quantity
* ### Product
  Used to insert, delete and view
  * Product name
  * Available Number
* ### Product Description
  Used to insert, delete and view
  * Product Id
  * Weight
  * Width
  * Colour
  * Height
* ### Product Group
  Used to insert, view and delete
  * Group Name
  * Group Id
* ### Payment
  Used to insert, view and delete
  * Payment Type
  * Credit Card number
  * Card type
  * CVV
  * Expiry Date
  * Card Holder name
* ### Voucher
  Used to insert, delete and view discount vouchers
  * Voucher id
  * Discount Percentage
* ### Zip Code
  Used to add, delete and view zip codes
  * City
  * Zipcode
  * State
* ### Review
  Used to insert, delete and view
  * Review Id
  * Product ID
  * Defect Percentage
  * Quality Rating

## Project Working:
This Project includes 14 total files including the main interface file and 13 files 1 for each table with their functionality explained in project description, Main interface file asks the user about the operation he/she wants to perform and then on user selection to insert in a particulat table, Program for that table is called and allows user to perform this operation, **Key feature of this project is that on a single click data gets Stored, Delete or viewed from two databases i.e.**
* PostGres
* Firestore

 

  


