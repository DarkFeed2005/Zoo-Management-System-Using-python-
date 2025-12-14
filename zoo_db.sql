CREATE DATABASE IF NOT EXISTS zoo_db;
USE zoo_db;

-- Users and roles
CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL, -- 'admin', 'zookeeper', 'ticketing'
  description VARCHAR(255)
);

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Enclosures
CREATE TABLE enclosures (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  type VARCHAR(100),
  capacity INT DEFAULT 0,
  location VARCHAR(100),
  notes TEXT
);

-- Animals
CREATE TABLE animals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tag_id VARCHAR(50) UNIQUE,
  name VARCHAR(100),
  species VARCHAR(100) NOT NULL,
  sex ENUM('Male','Female','Unknown') DEFAULT 'Unknown',
  dob DATE,
  enclosure_id INT,
  health_status VARCHAR(100) DEFAULT 'Healthy',
  last_checkup DATE,
  notes TEXT,
  FOREIGN KEY (enclosure_id) REFERENCES enclosures(id)
);

-- Feeding schedules
CREATE TABLE feed_schedules (
  id INT AUTO_INCREMENT PRIMARY KEY,
  animal_id INT NOT NULL,
  feed_item VARCHAR(100) NOT NULL,
  quantity VARCHAR(50),
  schedule_time TIME NOT NULL,
  frequency VARCHAR(50), -- e.g., Daily, Twice a day
  FOREIGN KEY (animal_id) REFERENCES animals(id)
);

-- Staff (optional separation from users)
CREATE TABLE staff (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  role_title VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100),
  user_id INT UNIQUE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tickets and pricing
CREATE TABLE ticket_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL, -- Adult, Child, Student
  price DECIMAL(10,2) NOT NULL,
  active TINYINT(1) DEFAULT 1
);

CREATE TABLE tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticket_type_id INT NOT NULL,
  buyer_name VARCHAR(100),
  issue_date DATE DEFAULT (CURRENT_DATE),
  issue_time TIME DEFAULT (CURRENT_TIME),
  quantity INT DEFAULT 1,
  total_price DECIMAL(10,2) NOT NULL,
  issued_by INT, -- users.id
  FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(id),
  FOREIGN KEY (issued_by) REFERENCES users(id)
);

-- Audit log
CREATE TABLE audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(100) NOT NULL, -- e.g., 'CREATE_ANIMAL', 'UPDATE_ENCLOSURE'
  entity VARCHAR(100), -- 'animals', 'enclosures'
  entity_id INT,
  details TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);