

import mysql.connector

from config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_SSL_CA
)


def get_connection():
    connection_config = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME
    }

    # Enable SSL for cloud database connections
    if DB_HOST not in ("localhost", "127.0.0.1"):
        connection_config["ssl_ca"] = DB_SSL_CA
        connection_config["ssl_verify_cert"] = True

    print(f"Connecting to MySQL on port: {DB_PORT}")

    return mysql.connector.connect(**connection_config)


def create_database():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                owner VARCHAR(255) NOT NULL,
                repository VARCHAR(255) NOT NULL,
                stars INT DEFAULT 0,
                forks INT DEFAULT 0,
                issues INT DEFAULT 0,
                language VARCHAR(100),
                health_score DECIMAL(10, 2),
                status VARCHAR(50),
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()

    finally:
        conn.close()


def save_repository(
    owner,
    repository,
    stars,
    forks,
    issues,
    language,
    score,
    status
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO repositories (
                owner,
                repository,
                stars,
                forks,
                issues,
                language,
                health_score,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            owner,
            repository,
            stars,
            forks,
            issues,
            language,
            score,
            status
        ))

        conn.commit()
        cursor.close()

    finally:
        conn.close()


def get_history():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                owner,
                repository,
                stars,
                forks,
                issues,
                language,
                health_score,
                status,
                searched_at
            FROM repositories
            ORDER BY searched_at DESC
        """)

        rows = cursor.fetchall()
        cursor.close()

        return rows

    finally:
        conn.close()

