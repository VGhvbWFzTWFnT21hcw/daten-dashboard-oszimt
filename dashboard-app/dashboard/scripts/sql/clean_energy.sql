-- clean_energy.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS cleaned_energy;

-- Create the dimension table from cleaned_sunshine
CREATE VIEW cleaned_energy AS 
SELECT 
    -- add ID column for faster joins
    ROW_NUMBER() OVER (ORDER BY timestamp) AS id_energy,
    -- original timestamp in string format
    -- convert to timestamp format and correct timezone
    -- 2025-01-01 00:00:00+0100
    timestamp::TIMESTAMPTZ AT TIME ZONE 'Europe/Gibraltar' AS timestamp,
    -- Change NULL values to 0 for numeric columns
    COALESCE(wind_onshore_mw,0) AS wind_onshore_mw,
    COALESCE(wind_offshore_mw,0) AS wind_offshore_mw,
    COALESCE(photovoltaics_mw,0) AS photovoltaics_mw,
    COALESCE(hydro_runofriver_mw,0) AS hydro_runofriver_mw,
    COALESCE(biomass_mw,0) AS biomass_mw,
    COALESCE(other_renewables_mw,0) AS other_renewables_mw,
    COALESCE(lignite_mw,0) AS lignite_mw,
    COALESCE(hard_coal_mw,0) AS hard_coal_mw,
    COALESCE(fossil_gas_mw,0) AS fossil_gas_mw,
    COALESCE(nuclear_mw,0) AS nuclear_mw,
    COALESCE(other_conventional_mw,0) AS other_conventional_mw,
    COALESCE(pumped_storage_generation_mw,0) AS pumped_storage_generation_mw,
    COALESCE(demand_mw,0) AS demand_mw,
    COALESCE(curtailment_or_exports_mw,0) AS curtailment_or_exports_mw,
    COALESCE(unserved_or_imports_mw,0) AS unserved_or_imports_mw,
    COALESCE(total_generation_mw,0) AS total_generation_mw

FROM raw_energy;
