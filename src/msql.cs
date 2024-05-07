            // Create the connection string using the specified values.
            string connectionString = $"Server={server};Database={database};Uid={username};Pwd={password};";

            // Create a connection to the database.
            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                // Open the connection.
                connection.Open();

                // Create a command to execute against the database.
                using (MySqlCommand command = connection.CreateCommand())
                {
                    // Set the command text.
                    command.CommandText = "SELECT * FROM users;";

                    // Execute the command and get the results.
                    using (MySqlDataReader reader = command.ExecuteReader())
                    {
                        // Read the results and print them to the console.
                        while (reader.Read())
                        {
                            Console.WriteLine($"{reader["id"]}, {reader["name"]}, {reader["email"]}");
                        }
                    }
                }
            }  
