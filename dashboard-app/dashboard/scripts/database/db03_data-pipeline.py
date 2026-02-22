import duckdb

# Connect to your database
con = duckdb.connect("duckdb/energy_data.duckdb")

# Install and load the icu extension
# Note: Extensions only need to be installed once per installation, 
# but must be loaded in every new session.
con.execute("INSTALL icu;")
con.execute("LOAD icu;")

# Helper function to read SQL files
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Read the SQL files
scripts = {
    "clean_energy": read_sql_file("dashboard-app/dashboard/scripts/sql/clean_energy.sql"),
    "clean_sunshine": read_sql_file("dashboard-app/dashboard/scripts/sql/clean_sunshine.sql"),
    "dim_time": read_sql_file("dashboard-app/dashboard/scripts/sql/dim_time.sql"),
    "dim_weather": read_sql_file("dashboard-app/dashboard/scripts/sql/dim_weather.sql"),
    "fact_generation": read_sql_file("dashboard-app/dashboard/scripts/sql/fact_generation.sql"),
    #"fact_usage": read_sql_file("dashboard-app/dashboard/scripts/sql/fact_usage.sql"),
    #"fact_sunshine": read_sql_file("dashboard-app/dashboard/scripts/sql/fact_sunshine.sql")
}

# Execute the queries
for script_name, sql_content in scripts.items():
    con.execute(sql_content)

# Verify the result
print("--- Tables Created ---")
# .df() converts the result directly to a Pandas DataFrame if installed
print(con.execute("SELECT * FROM fact_generation LIMIT 5").df())
print(con.execute("SELECT * FROM dim_time LIMIT 5").df()) 
print(con.execute("SELECT * FROM dim_weather LIMIT 5").df()) 
# Close the connection
con.close()
