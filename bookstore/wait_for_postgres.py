import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres():
    print("Waiting for Postgres...")
    while True:
        try:
            connection = psycopg2.connect(
                dbname="bookstore",
                user="bookstoreuser",
                password="1234",
                host="db",
                port="5432"
            )
            connection.close()
            print("Postgres is up - executing command")
            break
        except OperationalError as e:
            print(f"Postgres is unavailable - sleeping: {e}")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_postgres()
