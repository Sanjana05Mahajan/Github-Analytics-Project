
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


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