// create a c# function to connect to a mssql server using a local credential accessing three tables /order /customer /product and do a get and update on those tables

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;

namespace sqlserver
{
    class Program
    {
        static void Main(string[] args)
        {
            // Create a connection string.
            string connectionString = "Data Source=localhost;Initial Catalog=AdventureWorks2014;Integrated Security=True";

            // Create a connection to the database.
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                // Open the connection.
                connection.Open();

                // Create a command to get all orders.
                using (SqlCommand command = new SqlCommand("SELECT * FROM SalesLT.Orders", connection))
                {
                    // Execute the command.
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        // Read the results.
                        while (reader.Read())
                        {
                            Console.WriteLine("{0} {1} {2}",
                                reader.GetFieldValue<int>("OrderID"),
                                reader.GetFieldValue<string>("CustomerID"),
                                reader.GetFieldValue<DateTime>("OrderDate"));
                        }
                    }
                }

                // Create a command to get all customers.
                using (SqlCommand command = new SqlCommand("SELECT * FROM SalesLT.Customers", connection))
                {
                    // Execute the command.
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        // Read the results.
                        while (reader.Read())
                        {
                            Console.WriteLine("{0} {1} {2}",
                                reader.GetFieldValue<int>("CustomerID"),
                                reader.GetFieldValue<string>("FirstName"),
                                reader.GetFieldValue<string>("LastName"));
                        }
                    }
                }

                // Create a command to get all products.
                using (SqlCommand command = new SqlCommand("SELECT * FROM SalesLT.Products", connection))
                {
                    // Execute the command.
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        // Read the results.
                        while (reader.Read())
                        {
                            Console.WriteLine("{0} {1} {2}",
                                reader.GetFieldValue<int>("ProductID"),
                                reader.GetFieldValue<string>("ProductName"),
                                reader.GetFieldValue