README

This FastAPI application demonstrates how to connect to a PostgreSQL database using a service account. The application has a single endpoint that returns a list of orders for a given customer id.

Prerequisites

Python 3.6 or later
FastAPI
asyncpg
A PostgreSQL database
A service account with the necessary permissions to access the database
Installation

To install the required dependencies, run the following command:

pip install fastapi asyncpg
Usage

To run the application, run the following command:

uvicorn app:app --reload
You can then open your browser and navigate to http://localhost:8000/orders/1 to see a list of orders for customer id 1.

Security

The application uses a service account to connect to the database. This is a more secure way to connect to a database than using a hardcoded password. The service account credentials are stored in a secure location, and they are not shared with anyone.

The application also uses prepared statements to prevent SQL injection attacks. Prepared statements are a way to prevent SQL injection attacks by ensuring that the SQL query is executed with the correct parameters.

Next Steps

You can learn more about FastAPI by reading the documentation:

FastAPI documentation
FastAPI tutorial
You can also learn more about asyncpg by reading the documentation:

asyncpg documentation