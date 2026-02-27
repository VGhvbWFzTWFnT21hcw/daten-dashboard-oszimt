# --- STUFE 2: Vollständigkeit & Konsistenz ---

import duckdb

# Connect to database file
con = duckdb.connect("duckdb/energy_data.duckdb")

# 3. Vollständigkeit (Completeness)
# Abgleich der Zeitreihe auf Lücken im 15-Minuten-Raster
completeness_fact = con.sql("""
    WITH timerange AS (
        SELECT CAST(generate_series AS TIMESTAMP) as expected_ts
        FROM generate_series(
            (SELECT min(timestamp) FROM fact_generation),
            (SELECT max(timestamp) FROM fact_generation),
            interval '15 minutes'
        )
    )
    SELECT count(expected_ts) as missing_intervals
    FROM timerange
    LEFT JOIN fact_generation ON timerange.expected_ts = fact_generation.timestamp
    WHERE fact_generation.timestamp IS NULL
""").df()


# 4. Konsistenz (Consistency)
# Prüfen, ob die berechnete Summe der Energiequellen dem Gesamtverbrauch entspricht
consistency_fact = con.sql("""
    SELECT count(*) as inconsistent_rows
    FROM fact_generation
    WHERE abs(total_generation_mw - (renewable_mw + conventional_mw + pumped_storage_generation_mw)) > 0.4
""").df()

print(f"Core - Vollständigkeit (Fehlende Intervalle): {completeness_fact['missing_intervals'][0]}")
print(f"Core - Konsistenz (Rechenfehler Anteile): {consistency_fact['inconsistent_rows'][0]}")

# Close the connection
con.close()