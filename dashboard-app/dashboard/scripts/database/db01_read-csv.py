import duckdb

# Connect to the persistent database file
# If the file doesn't exist, it will be created automatically
con = duckdb.connect("duckdb/energy_data.duckdb")

# Import the CSV files into the database as permanent tables
# read_csv() auto-detects types and settings by default
con.execute("CREATE TABLE raw_energy AS SELECT * FROM read_csv('dashboard-app/dashboard/data/energiedaten.csv');")
con.execute("CREATE TABLE raw_sunshine AS SELECT * FROM read_csv('dashboard-app/dashboard/data/sonnenschein.csv');")

# To check if it's working, execute a query and fetch the results
result = con.execute("SELECT timestamp FROM raw_sunshine LIMIT 3;").fetchall()
print(result)
