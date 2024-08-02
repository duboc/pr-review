## crie uma conexão a um banco postgres usando usuario local e consulte dados de cliente e produto

import psycopg2

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myuser",
    password="mypassword"
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