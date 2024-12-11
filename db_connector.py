import os
from mysql import connector
import json

def get_database_schema_wrapper(db_obj, database_name):
    """Wrapper function to fetch and display database schema."""
    try:
        schema = get_database_schema(db_obj, database_name)
        if schema:
            print("Database Schema:")
            for table, columns in schema.items():
                print(f"Table: {table}")
                for column in columns:
                    print(f"  {column}")
        return schema
    except Exception as e:
        print(f"Error retrieving database schema: {e}")
        return None

def get_all_tables(db_obj, db_name="chatsql"):
    """Fetch all table names in the given database."""
    try:
        cursor = db_obj.cursor()
        cursor.execute(f"USE {db_name}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names
    except connector.Error as e:
        print(f"Error retrieving tables: {e}")
        return None
    finally:
        cursor.close()

def create_database(db_name="chatsql", host="localhost", user="root", password="root"):
    """Create a new database or connect to an existing one."""
    try:
        db = connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        return db
    except connector.Error as e:
        print(f"Database creation error: {e}")
        return None
    finally:
        cursor.close()

import mysql.connector

def execute_query(db_obj, query):
    try:
        cursor = db_obj.cursor()
        results = []
        queries = query.split(";")
        for q in queries:
            q = q.strip()
            if q:  
                cursor.execute(q)
                results.append(cursor.fetchall())
        cursor.close() 
        return results
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error in execute_query: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None



def get_database_schema(db_obj, db_name="chatsql"):
    """Retrieve the schema of the specified database."""
    try:
        cursor = db_obj.cursor()
        cursor.execute(f"USE {db_name}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema = {}
        for (table_name,) in tables:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            schema[table_name] = columns
        return schema
    except connector.Error as e:
        print(f"Error retrieving schema: {e}")
        return None
    finally:
        cursor.close()

# # Example Usage
# if __name__ == "__main__":
#     # Create a database connection
#     db_obj = create_database("chatsql", host="localhost", user="root", password="root")
#     if db_obj:
#         # Fetch database schema
#         schema = get_database_schema_wrapper(db_obj, "chatsql")
#         print("Schema:", schema)

#         # Example queries
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             username VARCHAR(255) NOT NULL,
#             email VARCHAR(255) NOT NULL UNIQUE,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#         """
#         execute_query(db_obj, create_table_query)

#         insert_query = """
#         INSERT INTO users (username, email)
#         VALUES ('Alice', 'alice@example.com'),
#                ('Bob', 'bob@example.com')
#         """
#         execute_query(db_obj, insert_query)

#         select_query = "SELECT * FROM users"
#         results = execute_query(db_obj, select_query)
#         print("Query Results:", results)

#         # Close the database connection
#         db_obj.close()
