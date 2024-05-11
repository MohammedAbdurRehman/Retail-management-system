# Retail Management System
## Overview:
Retail Management System is designed to manage data of employees, customers, product, orders and other aspects related to Retail Store listed below

## Purpose:
The primary purpose of the Retail Management System Database is to store and manage essential data for retail operations. This includes customer details such as names, addresses, contact information, as well as product information like product IDs, categories, and quantities. The database serves as a central repository for retail-related data, allowing for efficient retrieval and management.

## Key Features:
The key feature of our Management System is that along with managing the data on local machine using your localhost' database i.e. **Postgres** it also stores and manages data on a cloud based platform i.e. **Firebase-Firestore-Database** allowing to access the same data on multiple devices without any hastle
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
![image](https://github.com/MohammedAbdurRehman/Retail-management-system/assets/162794845/6caba491-8499-45a4-92aa-285fb9c119d8)

## Semantic Object Model Diagram:
![image](https://github.com/MohammedAbdurRehman/Retail-management-system/assets/162794845/2283b502-3ec5-4084-9def-6cc5700658e7)

## Database Project Architecture Diagram:
![image](https://github.com/MohammedAbdurRehman/Retail-management-system/assets/162794845/1dc8f404-b010-4902-a1bd-9be49ecbc90c)

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
This Project includes 14 total files including the main interface file and 13 files 1 for each table with their functionality explained in project description, Main interface file asks the user about the operation he/she wants to perform and then on user selection to insert in a particulat table, Program for that table is called and allows user to perform this operation.

 

  


