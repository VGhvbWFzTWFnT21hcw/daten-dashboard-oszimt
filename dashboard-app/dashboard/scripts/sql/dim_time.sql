-- dim_time.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS dim_time;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE dim_time AS 
SELECT DISTINCT 
    -- The original timestamp info
    timestamp AS full_timestamp,

    -- Extract specific dimensions
    timestamp::DATE AS date,
    extract('year' FROM timestamp)::SMALLINT AS year,
    extract('month' FROM timestamp)::TINYINT AS month,
    extract('day' FROM timestamp)::TINYINT AS day,
    extract('hour' FROM timestamp)::TINYINT AS hour,
    ((extract('isodow' FROM timestamp)::TINYINT) - 1) AS weekday

FROM cleaned_sunshine;
