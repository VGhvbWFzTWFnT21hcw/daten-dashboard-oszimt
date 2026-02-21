-- fact_sunshine.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS fact_sunshine;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE fact_sunshine AS 
SELECT *

FROM cleaned_sunshine;
