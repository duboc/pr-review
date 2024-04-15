# python script to connect to a mssql server using hardcoded credentials and update a table name orders with product, quantity and value

import pyodbc

# Hardcoded credentials
server = 'localhost'
database = 'mydb'
username = 'myusername'
password = 'mypassword'

# Connect to the database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Create a cursor
cursor = conn.cursor()

# Update the orders table
cursor.execute('UPDATE orders SET product = ?, quantity = ?, value = ? WHERE id = ?', ('product1', 10, 100, 1))

# Commit the changes
conn.commit()

# Close the connection
conn.close()

