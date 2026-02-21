import duckdb

# Define the database file path
db_file = "duckdb/energy_data.duckdb"

# Create a connection to the persistent database
# This is the functional equivalent of connection_open()
con = duckdb.connect(db_file)

# To check if it's working
# Use .execute() to run the query and .fetchall() to see the results
result = con.execute("SELECT timestamp FROM raw_sunshine LIMIT 3;").fetchall()

for row in result:
    print(row)
