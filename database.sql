-- Zoo Management System Schema (Plain Passwords)
-- Author: KpolitX
-- Date: December 2025

-- ===========================
-- USERS TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,   -- plain text password
    role ENUM('admin', 'zookeeper', 'ticketing') NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- ===========================
-- ENCLOSURES TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS enclosures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    capacity INT DEFAULT 10,
    current_occupancy INT DEFAULT 0,
    location VARCHAR(200),
    status ENUM('Active', 'Maintenance', 'Closed') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================
-- ANIMALS TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS animals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    gender ENUM('Male', 'Female', 'Unknown'),
    enclosure_id INT,
    health_status ENUM('Healthy', 'Sick', 'Under Treatment', 'Critical') DEFAULT 'Healthy',
    last_checkup DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (enclosure_id) REFERENCES enclosures(id) ON DELETE SET NULL
);

-- ===========================
-- FEEDING SCHEDULES TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS feeding_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    feed_time TIME NOT NULL,
    food_type VARCHAR(100),
    quantity VARCHAR(50),
    frequency ENUM('Daily', 'Twice Daily', 'Weekly', 'Custom') DEFAULT 'Daily',
    notes TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ===========================
-- TICKETS TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_type VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT
);

-- ===========================
-- SALES TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_amount DECIMAL(10, 2) NOT NULL,
    customer_name VARCHAR(100),
    sold_by INT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (sold_by) REFERENCES users(id)
);

-- ===========================
-- AUDIT LOGS TABLE
-- ===========================
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ===========================
-- INDEXES
-- ===========================
CREATE INDEX idx_animals_enclosure_id ON animals(enclosure_id);
CREATE INDEX idx_sales_ticket_id ON sales(ticket_id);
CREATE INDEX idx_sales_sold_by ON sales(sold_by);

-- ===========================
-- SEED DATA
-- ===========================

-- Admin User (plain password)
INSERT IGNORE INTO users (username, password, role, full_name, email)
VALUES ('admin', 'admin123', 'admin', 'System Administrator', 'admin@zoo.com');

-- Tickets
INSERT IGNORE INTO tickets (id, ticket_type, price, description) VALUES
(1, 'Adult', 25.00, 'Adult entry ticket'),
(2, 'Child', 15.00, 'Child entry ticket (3-12 years)'),
(3, 'Senior', 20.00, 'Senior citizen ticket (60+)'),
(4, 'Family Pack', 70.00, 'Family pack (2 adults + 2 children)');

-- Enclosures
INSERT IGNORE INTO enclosures (id, name, type, capacity, location, status) VALUES
(1, 'Savanna Habitat', 'Open Range', 15, 'North Zone', 'Active'),
(2, 'Primate House', 'Indoor', 8, 'East Zone', 'Active'),
(3, 'Aquarium', 'Water', 30, 'South Zone', 'Active');