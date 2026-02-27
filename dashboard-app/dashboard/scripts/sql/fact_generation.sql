-- fact_generation.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS fact_generation;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE fact_generation AS 
WITH calculated_sums AS (
    SELECT 
        *,
        (wind_onshore_mw + 
        wind_offshore_mw + 
        photovoltaics_mw + 
        hydro_runofriver_mw + 
        biomass_mw + 
        other_renewables_mw) AS renewable_mw,
        (lignite_mw + 
        hard_coal_mw + 
        fossil_gas_mw + 
        nuclear_mw + 
        other_conventional_mw) AS conventional_mw
    FROM cleaned_energy
),

SELECT 
    COALESCE(ce.id_energy, sun.id_sun) AS id,
    ce.*,
    sun.id_sun,
    sun.sunshine_minutes_15min,
    ROUND((ce.renewable_mw / NULLIF(ce.total_generation_mw, 0)) * 100, 1) AS renewable_share
FROM calculated_sums ce
FULL OUTER JOIN cleaned_sunshine sun ON ce.id_energy = sun.id_sun;