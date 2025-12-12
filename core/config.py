import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "sql10.freesqldatabase.com"),
    "user": os.getenv("DB_USER", "sql10811613"),
    "password": os.getenv("DB_PASSWORD", "uzZca1iqXD"),
    "database": os.getenv("DB_NAME", "sql10811613"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

APP = {
    "name": "Zoo Manager",
    "version": "1.0.0"
}