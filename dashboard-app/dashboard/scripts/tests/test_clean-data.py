import duckdb

# 1. Connect to an existing database file
con = duckdb.connect("duckdb/energy_data.duckdb")

# Reference tables (similar to tbl(con, ...))
t1 = con.table("raw_sunshine")

# 2. Data Transformation
# DuckDB's Python API allows method chaining similar to dplyr's %>%
table1_cleaned = t1.project("""
    strptime(timestamp::VARCHAR, '%Y-%m-%d %H:%M:%S%z') AS timestamp,
    coalesce(sunshine_minutes_15min, 0) AS sunshine_minutes_15min
""").filter("timestamp IS NOT NULL")

# 3. Data Quality Checks
# Check A: Uniqueness (Identify duplicate IDs)
duplicates = t1.aggregate("timestamp, count(*) AS n", "timestamp") \
               .filter("n > 1") \
               .df()  # .df() is equivalent to collect()

# Check D: Freshness
freshness = table1_cleaned.aggregate("max(timestamp) AS latest_entry").df()

# 4. Output Results
print("--- Data Quality Summary ---")
print(f"Duplicate IDs found: {len(duplicates)}")
print(f"Latest record timestamp: {freshness['latest_entry'][0]}")

# 5. Save Cleaned Data
# Equivalent to compute(name = "cleaned_sunshine", temporary = False)
# This creates a persistent table from the transformation pipeline
con.execute("DROP TABLE IF EXISTS cleaned_sunshine")
table1_cleaned.create("cleaned_sunshine")

# Close connection
con.close()
