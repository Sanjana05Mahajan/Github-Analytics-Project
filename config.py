
import os

BASE_URL = "https://api.github.com"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "github_analytics")
DB_SSL_CA = os.getenv("DB_SSL_CA", "certificates/ca.pem")

DEBUG = False
