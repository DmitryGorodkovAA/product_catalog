import os
import sys
import psycopg2
ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)

from infrastructure.config import Config
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

def run_migrations():
    conn = psycopg2.connect(Config.DATABASE_URL)
    cur = conn.cursor()

    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

    cur.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) UNIQUE,
            applied_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()

    for file in files:
        cur.execute("SELECT 1 FROM migrations WHERE filename=%s", (file,))
        if cur.fetchone():
            continue

        print(f"Applying migration: {file}")
        with open(os.path.join(MIGRATIONS_DIR, file), "r") as f:
            sql = f.read()
            cur.execute(sql)
        cur.execute("INSERT INTO migrations (filename) VALUES (%s)", (file,))
        conn.commit()

    cur.close()
    conn.close()
    print("All migrations applied!")

if __name__ == "__main__":
    run_migrations()
