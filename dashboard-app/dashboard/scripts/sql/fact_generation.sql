-- fact_generation.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS fact_generation;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE fact_generation AS 
SELECT 
    timestamp,
    wind_onshore_mw,
    wind_offshore_mw,
    photovoltaics_mw,
    hydro_runofriver_mw,
    biomass_mw,
    other_renewables_mw,
    lignite_mw,
    hard_coal_mw,
    fossil_gas_mw,
    nuclear_mw,
    other_conventional_mw,
    (wind_onshore_mw + 
    wind_offshore_mw + 
    photovoltaics_mw + 
    hydro_runofriver_mw +
    biomass_mw + 
    other_renewables_mw) AS total_renewables,
    (lignite_mw + 
    hard_coal_mw + 
    fossil_gas_mw + 
    nuclear_mw +
    other_conventional_mw) AS total_conventional
    -- renewable_share

FROM cleaned_energy;
