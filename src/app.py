from fastapi import FastAPI, Path
from typing import List
import asyncpg

app = FastAPI()

@app.get("/orders/{customer_id}", response_model=List[Order])
async def get_orders(customer_id: int = Path(...)):
    # Load the service account credentials from a file
    credentials = asyncpg.Credentials.from_service_account_file("service-account.json")

    # Connect to the PostgreSQL database using the service account credentials
    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        user=credentials.user,
        password=credentials.password,
        database="my-database",
    )

    # Query the database to get the orders for the given customer id
    orders = await conn.fetch(
        "SELECT * FROM orders WHERE customer_id = $1",
        customer_id,
    )

    # Close the connection to the database
    await conn.close()

    # Return the list of orders
    return orders
