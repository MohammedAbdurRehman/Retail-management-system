
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
AFTER INSERT ON Order_Product
FOR EACH ROW
EXECUTE FUNCTION update_product_availability();


CREATE OR REPLACE FUNCTION calculate_order_total(order_id VARCHAR)
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL := 0;
BEGIN
    SELECT SUM(op.Quantity * p.Price)
    INTO total
    FROM Order_Product op
    JOIN Product p ON op.Product_ID = p.ProductID
    WHERE op.Order_ID = order_id;
    RETURN total;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_order_status(order_id VARCHAR, new_status VARCHAR)
AS $$
BEGIN
    UPDATE Orders
    SET Status = new_status
    WHERE Order_ID = order_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION generate_voucher_on_large_order()
RETURNS TRIGGER AS $$
DECLARE
    order_total DECIMAL;
BEGIN
    order_total := calculate_order_total(NEW.Order_ID);
    IF order_total > 500 THEN
        INSERT INTO Voucher (Voucher_ID, Discount_percent)
        VALUES ('V' || NEW.Order_ID, 10); -- 10% discount voucher
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER generate_voucher_trigger
AFTER INSERT ON Orders
FOR EACH ROW
EXECUTE FUNCTION generate_voucher_on_large_order();


CREATE OR REPLACE FUNCTION calculate_average_product_rating(product_id VARCHAR)
RETURNS DECIMAL AS $$
DECLARE
    avg_rating DECIMAL;
BEGIN
    SELECT AVG(Quality)
    INTO avg_rating
    FROM Review
    WHERE ProductID = product_id;
    RETURN avg_rating;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE process_returns(order_id VARCHAR)
AS $$
DECLARE
    returned_quantity INT;
BEGIN
    -- Assume returned_quantity is obtained from user input or another process
    returned_quantity := 1; -- Example: Assume 1 item returned

    -- Update Order status to Returned
    update_order_status(order_id, 'Returned');

    -- Adjust product availability
    UPDATE Product
    SET Available_Number = Available_Number + returned_quantity
    WHERE ProductID IN (
        SELECT Product_ID
        FROM Order_Product
        WHERE Order_ID = order_id
    );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_product_group()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Product_Name ILIKE '%electronics%' THEN
        INSERT INTO Product_Group (Group_Name)
        VALUES ('Electronics');
    ELSIF NEW.Product_Name ILIKE '%clothing%' THEN
        INSERT INTO Product_Group (Group_Name)
        VALUES ('Clothing');
    ELSIF NEW.Product_Name ILIKE '%shoes%' THEN
        INSERT INTO Product_Group (Group_Name)
        VALUES ('Shoes');
    ELSE
        INSERT INTO Product_Group (Group_Name)
        VALUES ('Other');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_product_group_trigger
AFTER INSERT ON Product
FOR EACH ROW
EXECUTE FUNCTION update_product_group();





