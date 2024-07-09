import pandas as pd
import pyodbc
import csv
class Database:

    def __init__(self):
        print("Database init")
        self.server = "obrechtstudios.de"
        self.database = "AvA"
        self.username = "princeofdarkness"
        self.password = "dxr74z3H69"
        self.driver = "ODBC Driver 17 for SQL Server"
        self.conn = self._create_connection()
        print("Database Connected")

    def _create_connection(self):
        conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    # Key Value Store

    def set_key_value(self, table_name, key, value):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE {table_name} SET item_value = ? WHERE item_key = ?
        ''', (value, key))
        self.conn.commit()

    def get_value_key_value_store(self, table_name, key):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            SELECT item_value FROM {table_name}
            WHERE item_key = ?
        ''', (key,))
        result = cursor.fetchone()
        return result[0] if result else None
