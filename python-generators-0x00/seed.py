import mysql.connector
import csv

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""  # replace with your MySQL root password if set
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # replace if needed
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    print("Data inserted successfully")
    cursor.close()
