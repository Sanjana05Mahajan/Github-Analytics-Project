
import os

BASE_URL = "https://api.github.com"

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = "github_analytics"

DEBUG = True