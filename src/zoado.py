import psycopg2
import os

# Use environment variables for sensitive information
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Cria um cursor
cur = conn.cursor()

# Executa uma consulta SQL para selecionar dados de clientes
cur.execute("SELECT * FROM customers")

# Recupera todos os resultados da consulta
customers = cur.fetchall()

# Imprime os dados dos clientes
print("Clientes:")
for customer in customers:
    print(f"ID: {customer[0]}, Nome: {customer[1]}, Email: {customer[2]}")

# Executa uma consulta SQL para selecionar dados de produtos
cur.execute("SELECT * FROM products")

# Recupera todos os resultados da consulta
products = cur.fetchall()

# Imprime os dados dos produtos
print("\nProdutos:")
for product in products:
    print(f"ID: {product[0]}, Nome: {product[1]}, Preço: {product[2]}")

# Fecha o cursor e a conexão
cur.close()
conn.close()
