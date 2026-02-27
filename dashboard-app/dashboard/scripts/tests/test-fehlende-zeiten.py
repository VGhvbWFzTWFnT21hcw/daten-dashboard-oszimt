# Konsistenz-Fehler im Detail

import duckdb

# Connect to database file
con = duckdb.connect("duckdb/energy_data.duckdb") 

consistency_errors = con.sql("""
    SELECT 
        timestamp, 
        total_generation_mw, 
        renewable_mw, 
        conventional_mw,
        abs(total_generation_mw - (renewable_mw + conventional_mw + pumped_storage_generation_mw)) as difference
    FROM fact_generation
    WHERE abs(total_generation_mw - (renewable_mw + conventional_mw + pumped_storage_generation_mw)) > 0.21
""").df()

if not consistency_errors.empty:
    print("--- Konsistenz-Fehler gefunden: ---")
    print(consistency_errors)
else:
    print("Keine Konsistenz-Fehler gefunden.")


# Vollständigkeits-Lücken im Detail
missing_timestamps = con.sql("""
    WITH timerange AS (
        SELECT CAST(generate_series AS TIMESTAMP) as expected_ts
        FROM generate_series(
            (SELECT min(timestamp) FROM fact_generation),
            (SELECT max(timestamp) FROM fact_generation),
            interval '15 minutes'
        )
    )
    SELECT timerange.expected_ts as missing_timestamp
    FROM timerange
    LEFT JOIN fact_generation ON timerange.expected_ts = fact_generation.timestamp
    WHERE fact_generation.timestamp IS NULL
    ORDER BY timerange.expected_ts
""").df()

if not missing_timestamps.empty:
    print("--- Fehlende Zeitstempel (Lücken): ---")
    print(missing_timestamps)
else:
    print("Keine Lücken in der Zeitreihe gefunden.")

# Close the connection
con.close()