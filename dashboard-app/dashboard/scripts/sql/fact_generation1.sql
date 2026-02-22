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
)
SELECT 
    *,
    -- Calculate share: (Renewable / Total) * 100 rounded to 1 decimal
    ROUND((renewable_mw / NULLIF(total_generation_mw, 0)) * 100, 1) AS renewable_share
FROM calculated_sums;