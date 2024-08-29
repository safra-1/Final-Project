import mysql.connector

def create_data_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="news"  # No non-printable characters here
        )

        print("MySQL Database connection successful")
        return connection
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Replace the placeholder values with your actual connection details
conn = create_data_connection()
if conn is not None:
    # Use the connection to perform database operations
    cursor = conn.cursor()
    # ... your database operations here ...
    cursor.close()
    conn.close()