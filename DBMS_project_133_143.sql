USE `library2`;

-- Create `books` table
CREATE TABLE `books` (
    `bookid` VARCHAR(20) NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `author` VARCHAR(100) NOT NULL,
    `status` VARCHAR(20) NOT NULL,
    `genre` VARCHAR(50) DEFAULT NULL,
    PRIMARY KEY (`bookid`)
);

-- Create `books_issued` table
CREATE TABLE `books_issued` (
    `bookid` VARCHAR(20) NOT NULL,
    `issueto` VARCHAR(100) DEFAULT NULL,
    `issue_date` DATE DEFAULT NULL,
    `return_date` DATE DEFAULT NULL,
    `fare` DECIMAL(10,2) DEFAULT NULL,
    `issue_time` TIME DEFAULT NULL,
    PRIMARY KEY (`bookid`),
    CONSTRAINT `fk_books_issued_bookid` FOREIGN KEY (`bookid`) 
        REFERENCES `books` (`bookid`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_books_issued_issueto` FOREIGN KEY (`issueto`) 
        REFERENCES `customer_credentials` (`username`) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Create `book_logs` table
CREATE TABLE `book_logs` (
    `log_id` INT NOT NULL AUTO_INCREMENT,
    `bookid` VARCHAR(20) DEFAULT NULL,
    `title` VARCHAR(100) DEFAULT NULL,
    `author` VARCHAR(100) DEFAULT NULL,
    `genre` VARCHAR(50) DEFAULT NULL,
    `action_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`log_id`),
    KEY `idx_bookid` (`bookid`),
    CONSTRAINT `fk_book_logs_bookid` FOREIGN KEY (`bookid`) 
        REFERENCES `books` (`bookid`) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Create `admin_credentials` table
CREATE TABLE `admin_credentials` (
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`username`)
);

-- Create `customer_credentials` table
CREATE TABLE `customer_credentials` (
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`username`)
);

-- Create `fare` table
CREATE TABLE `fare` (
    `fare_id` INT NOT NULL AUTO_INCREMENT,
    `fare_value` DECIMAL(10,2) DEFAULT NULL,
    `issue_to` VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (`fare_id`),
    KEY `idx_issue_to` (`issue_to`),
    CONSTRAINT `fk_fare_issue_to` FOREIGN KEY (`issue_to`) 
        REFERENCES `customer_credentials` (`username`) ON DELETE SET NULL ON UPDATE CASCADE
);

DELIMITER //

-- Trigger: Log new book insertions into `book_logs`
CREATE TRIGGER `book_insert_logger`
AFTER INSERT ON `books`
FOR EACH ROW
BEGIN
    INSERT INTO book_logs (bookid, title, author, genre)
    VALUES (NEW.bookid, NEW.title, NEW.author, NEW.genre);
END//

-- Trigger: Update book status to 'issued' after issuing a book
CREATE TRIGGER `update_status_on_issue`
AFTER INSERT ON `books_issued`
FOR EACH ROW
BEGIN
    UPDATE books
    SET status = 'issued'
    WHERE bookid = NEW.bookid;
END//

-- Trigger: Insert fare record after issuing a book
CREATE TRIGGER `after_books_issued_insert`
AFTER INSERT ON `books_issued`
FOR EACH ROW
BEGIN
    INSERT INTO fare (fare_value, issue_to)
    VALUES (NEW.fare, NEW.issueto);
END//

-- Trigger: Update book status to 'available' after book return
CREATE TRIGGER `update_status_on_return`
AFTER DELETE ON `books_issued`
FOR EACH ROW
BEGIN
    UPDATE books
    SET status = 'avail'
    WHERE bookid = OLD.bookid;
END//

DELIMITER ;

-- Stored Procedure: Get book details by ID
DELIMITER //
CREATE PROCEDURE `GetBookDetailsById`(
    IN p_bookid VARCHAR(20)
)
BEGIN
    SELECT 
        b.bookid,
        b.title,
        b.author,
        b.status,
        b.genre,
        bi.issueto,
        bi.issue_date,
        bi.return_date,
        bi.fare
    FROM books b
    LEFT JOIN books_issued bi ON b.bookid = bi.bookid
    WHERE b.bookid = p_bookid;
END//
DELIMITER ;

-- Stored Procedure: Register a new admin
DELIMITER //
CREATE PROCEDURE `RegisterAdmin`(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE user_exists INT;
    SELECT COUNT(*) INTO user_exists 
    FROM admin_credentials 
    WHERE username = p_username;
    IF user_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username already exists';
    ELSE
        INSERT INTO admin_credentials (username, password)
        VALUES (p_username, SHA2(p_password, 256));
    END IF;
END//
DELIMITER ;

-- Stored Procedure: Register a new customer
DELIMITER //
CREATE PROCEDURE `RegisterCustomer`(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE user_exists INT;
    SELECT COUNT(*) INTO user_exists 
    FROM customer_credentials 
    WHERE username = p_username;
    IF user_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username already exists';
    ELSE
        INSERT INTO customer_credentials (username, password)
        VALUES (p_username, SHA2(p_password, 256));
    END IF;
END//
DELIMITER ;

-- Stored Procedure: Verify admin credentials
DELIMITER //
CREATE PROCEDURE `VerifyAdminCredentials`(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    OUT p_is_valid BOOLEAN
)
BEGIN
    DECLARE stored_password VARCHAR(255);
    SELECT password INTO stored_password 
    FROM admin_credentials 
    WHERE username = p_username;
    IF stored_password IS NULL THEN
        SET p_is_valid = FALSE;
    ELSE
        SET p_is_valid = (stored_password = SHA2(p_password, 256));
    END IF;
END//
DELIMITER ;

-- Stored Procedure: Verify customer credentials
DELIMITER //
CREATE PROCEDURE `VerifyCustomerCredentials`(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    OUT p_is_valid BOOLEAN
)
BEGIN
    DECLARE stored_password VARCHAR(255);
    SELECT password INTO stored_password 
    FROM customer_credentials 
    WHERE username = p_username;
    IF stored_password IS NULL THEN
        SET p_is_valid = FALSE;
    ELSE
        SET p_is_valid = (stored_password = SHA2(p_password, 256));
    END IF;
END//
DELIMITER ;

-- Nested Query
SELECT status 
FROM books 
WHERE bookid = 'B022' 
AND status IN ('avail', 'available', 'AVAILABLE', 'Available');

-- Join Query
SELECT 
    b.bookid, 
    b.title, 
    b.author, 
    b.status, 
    COALESCE(bi.issueto, '-') AS issued_to,
    COALESCE(DATE_FORMAT(bi.issue_date, '%Y-%m-%d'), '-') AS issue_date,
    COALESCE(DATE_FORMAT(bi.return_date, '%Y-%m-%d'), '-') AS return_date,
    COALESCE(bi.fare, 0.00) AS fare
FROM books b
LEFT JOIN books_issued bi ON b.bookid = bi.bookid;

-- Aggregate Query
SELECT COUNT(*) AS books_issued_count 
FROM books_issued 
WHERE issueto = 'Samar';


