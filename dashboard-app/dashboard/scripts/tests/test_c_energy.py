import duckdb

# Connect to your database
# This creates a persistent connection to the file
con = duckdb.connect("duckdb/energy_data.duckdb")

# Install and load the icu extension
# These commands are executed directly via the connection object
con.execute("INSTALL icu;")
con.execute("LOAD icu;")

# Read the SQL file
# 'with' ensures the file is closed automatically after reading
with open("dashboard-app/dashboard/scripts/sql/clean_energy.sql", "r") as file:
    sql_query = file.read()

# Execute the query
con.execute(sql_query)

# Verify the result
print("--- Table Created ---")
# .df() returns a Pandas DataFrame, which is the Python equivalent of a data frame
print(con.execute("SELECT * FROM cleaned_energy LIMIT 5").df())

# Close the connection
con.close()
