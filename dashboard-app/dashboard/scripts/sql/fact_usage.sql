-- fact_usage.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS fact_usage;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE fact_usage AS 
SELECT 
    timestamp,
    pumped_storage_generation_mw,
    demand_mw,
    curtailment_or_exports_mw,
    unserved_or_imports_mw,
    total_generation_mw

FROM cleaned_energy;
