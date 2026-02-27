
import duckdb

# Create an in-memory database
con = duckdb.connect(database=':memory:')

# Run a simple query
result = con.execute("SELECT 'DuckDB is ready!'").fetchone()
print(result[0])

# Close the connection
con.close()