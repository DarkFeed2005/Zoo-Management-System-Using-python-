# 🦁 Zoo Management System

A comprehensive desktop application for managing zoo operations with role-based access control, built with Python, CustomTkinter, and MySQL.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📸 Screenshots

<!-- Add your screenshots here -->
- Modern dark-themed interface
- Role-based dashboard views
- Comprehensive data management

## ✨ Features

### 🔐 Role-Based Access Control (RBAC)
- **Admin**: Complete system access - manage all resources, users, and view audit logs
- **Zookeeper**: Animal care focused - manage animals, feeding schedules, and health records
- **Ticketing**: Sales operations - handle ticket sales, pricing, and daily reports

### 🎯 Core Modules
- **🦁 Animals Management**: Track animal records, health status, and enclosure assignments
- **🏛️ Enclosures Management**: Manage habitats, capacity tracking, and locations
- **🍖 Feeding Schedules**: Create and maintain feeding routines with time management
- **🎫 Ticket Sales System**: Real-time ticket sales with pricing and revenue tracking
- **👥 User Management**: Create users, assign roles, and manage system access
- **📊 Dashboard**: Live statistics, recent activity, and key performance indicators

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0 or higher** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/downloads/)

### Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/zoo-management-system.git
cd zoo-management-system
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Setup MySQL Database

1. **Start MySQL Server**
   - Windows: Start MySQL from Services or MySQL Workbench
   - macOS: `brew services start mysql`
   - Linux: `sudo systemctl start mysql`

2. **Create Database**

Open MySQL command line or MySQL Workbench and run:

```bash
mysql -u root -p < setup_database.sql
```

Or manually in MySQL:
```sql
source setup_database.sql;
```

This will:
- Create `zoo_db` database
- Create all required tables
- Insert default roles (admin, zookeeper, ticketing)
- Create default admin user
- Populate sample data (animals, enclosures, tickets)

#### Step 5: Configure Environment Variables

1. **Copy the example environment file:**

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

2. **Edit `.env` file with your MySQL credentials:**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=zoo_db
```

⚠️ **Important**: Replace `your_mysql_password_here` with your actual MySQL root password.

#### Step 6: Create Package Structure

Ensure all `__init__.py` files exist:

**Windows PowerShell:**
```powershell
New-Item -ItemType File -Path config/__init__.py, services/__init__.py, gui/__init__.py, gui/views/__init__.py -Force
```

**macOS/Linux:**
```bash
touch config/__init__.py services/__init__.py gui/__init__.py gui/views/__init__.py
```

#### Step 7: Run the Application

```bash
python app.py
```

### 🔑 Default Login Credentials

```
Username: admin
Password: admin123
```

⚠️ **Security Note**: Please change the default password immediately after first login!

## 📁 Project Structure

```
zoo-management-system/
│
├── app.py                          # Application entry point
│
├── config/                         # Configuration modules
│   ├── __init__.py
│   ├── database.py                 # Database connection and pooling
│   └── settings.py                 # Application settings and environment variables
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py             # Authentication and password management
│   └── rbac_service.py             # Role-based access control
│
├── gui/                            # User interface components
│   ├── __init__.py
│   ├── login_window.py             # Login interface
│   ├── main_dashboard.py           # Main application dashboard
│   └── views/                      # Feature-specific views
│       ├── __init__.py
│       ├── dashboard_view.py       # Statistics and overview
│       ├── animals_view.py         # Animal management
│       ├── enclosures_view.py      # Enclosure management
│       ├── feeding_view.py         # Feeding schedule management
│       ├── tickets_view.py         # Ticket sales interface
│       └── users_view.py           # User management (Admin only)
│
├── .env.example                    # Environment variables template
├── .env                            # Your environment variables (not in git)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── setup_database.sql              # Database initialization script
└── README.md                       # This file
```

## 🗄️ Database Schema

### Core Tables

- **roles** - User role definitions (admin, zookeeper, ticketing)
- **users** - System users with authentication and role assignments
- **animals** - Animal records with health information
- **enclosures** - Habitat/enclosure information
- **feed_schedules** - Feeding schedule and routines
- **tickets** - Ticket sales transactions
- **ticket_types** - Ticket pricing and types
- **staff** - Staff member information
- **audit_logs** - System activity audit trail

## 🎮 Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Manage Users**: Create accounts for zookeepers and ticketing staff
3. **Oversee Operations**: Monitor all activities through the dashboard
4. **Generate Reports**: Access comprehensive system reports
5. **Review Audit Logs**: Track all system changes

### For Zookeepers

1. **Login** with zookeeper credentials
2. **Manage Animals**: Update health records and notes
3. **Feeding Schedules**: Create and maintain feeding routines
4. **Monitor Health**: Track animal wellness and checkup dates

### For Ticketing Staff

1. **Login** with ticketing credentials
2. **Sell Tickets**: Process customer ticket purchases
3. **View Sales**: Monitor daily sales and revenue
4. **Manage Pricing**: Update ticket types and prices

## 🔧 Configuration

### Environment Variables

Edit the `.env` file to configure:

```env
# Database Configuration
DB_HOST=localhost          # MySQL host (default: localhost)
DB_PORT=3306              # MySQL port (default: 3306)
DB_USER=root              # MySQL username
DB_PASSWORD=your_password # MySQL password
DB_NAME=zoo_db            # Database name
```

### Application Settings

Edit `config/settings.py` for additional configuration:

- Window dimensions
- Security settings (bcrypt rounds)
- Application metadata

## 🔨 Building Standalone Executable

Create a standalone executable for distribution:

### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name="ZooManager" --icon=icon.ico app.py
```

The executable will be created in `dist/ZooManager.exe`

### macOS

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="ZooManager" app.py
```

### Linux

```bash
pip install pyinstaller
pyinstaller --onefile --name="ZooManager" app.py
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### "Can't connect to MySQL server"

**Solution:**
1. Verify MySQL is running: `mysql --version`
2. Check credentials in `.env` file
3. Test connection: `mysql -u root -p`
4. Ensure MySQL port 3306 is not blocked by firewall

#### "No module named 'customtkinter'"

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### "Database 'zoo_db' doesn't exist"

**Solution:**
```bash
mysql -u root -p < setup_database.sql
```

#### "Login failed" with correct credentials

**Solution:**
Reset admin password in MySQL:
```sql
USE zoo_db;
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NAQzjZBzWKka' 
WHERE username = 'admin';
```

#### ImportError or Module Not Found

**Solution:**
Ensure all `__init__.py` files exist:
```bash
# Windows
type nul > config\__init__.py
type nul > services\__init__.py
type nul > gui\__init__.py
type nul > gui\views\__init__.py

# macOS/Linux
touch config/__init__.py services/__init__.py gui/__init__.py gui/views/__init__.py
```

## 🔒 Security Features

- ✅ **Password Hashing**: bcrypt with salt for secure password storage
- ✅ **SQL Injection Prevention**: Parameterized queries throughout
- ✅ **Role-Based Access**: Granular permission system
- ✅ **Session Management**: Secure user session handling
- ✅ **Audit Logging**: Complete activity tracking
- ✅ **Connection Pooling**: Secure and efficient database connections

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Development Roadmap

### Planned Features

- [ ] Advanced reporting with data visualization
- [ ] Export functionality (PDF, Excel, CSV)
- [ ] Email notification system
- [ ] Visitor check-in/check-out system
- [ ] Veterinary appointment scheduling
- [ ] Inventory management for food and supplies
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] QR code ticket generation
- [ ] Analytics dashboard with charts

## 📋 Requirements

### Python Packages

```
customtkinter==5.2.1          # Modern UI framework
mysql-connector-python==8.2.0 # MySQL database driver
python-dotenv==1.0.0          # Environment variable management
bcrypt==4.1.2                 # Password hashing
Pillow==10.1.0                # Image processing
pyinstaller==6.3.0            # Executable builder (optional)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- **CustomTkinter** - Modern and customizable GUI framework
- **MySQL** - Robust database management system
- **bcrypt** - Secure password hashing library
- **Python Community** - For excellent documentation and support

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search [existing issues](https://github.com/yourusername/zoo-management-system/issues)
3. Create a [new issue](https://github.com/yourusername/zoo-management-system/issues/new) with:
   - Detailed description of the problem
   - Steps to reproduce
   - Your environment (OS, Python version, MySQL version)
   - Error messages or screenshots

## ⭐ Star This Repository

If you find this project useful, please give it a star! It helps others discover the project.

---

**Made with ❤️ using Python and CustomTkinter**

**Default Credentials**: admin / admin123 (Change immediately after first login!)
