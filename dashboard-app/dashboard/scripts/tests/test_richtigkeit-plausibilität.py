# --- STUFE 1: Richtigkeit & Plausibilität ---
import duckdb

# Connect to database file
con = duckdb.connect("duckdb/energy_data.duckdb")


# 1. Richtigkeit (Accuracy)
# Prüfen, ob Pflichtfelder (Timestamp) befüllt und Datentypen korrekt sind
accuracy_energy = con.sql("""
    SELECT count(*) as invalid_records
    FROM cleaned_energy
    WHERE timestamp IS NULL OR typeof(total_generation_mw) NOT IN ('DECIMAL', 'DOUBLE', 'FLOAT')
""").df()


# 2. Plausibilität (Plausibility)
# Prüfen auf physikalisch unmögliche Werte (negativ) oder unrealistische Spitzen
plausibility_energy = con.sql("""
    SELECT count(*) as outliers
    FROM cleaned_energy
    WHERE total_generation_mw < 0
""").df()

print(f"Staging - Richtigkeit (Ungültige Datensätze): {accuracy_energy['invalid_records'][0]}")
print(f"Staging - Plausibilität (Ausreißer/Negativ): {plausibility_energy['outliers'][0]}")

# Close the connection
con.close()
