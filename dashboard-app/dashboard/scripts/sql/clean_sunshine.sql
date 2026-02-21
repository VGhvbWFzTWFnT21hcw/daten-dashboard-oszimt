-- clean_sunshine.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS cleaned_sunshine;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE cleaned_sunshine AS 
SELECT 
    -- original timestamp in string format
    -- convert to timestamp format and correct timezone
    -- 2025-01-01 00:00:00+0100
    timestamp::TIMESTAMPTZ AT TIME ZONE 'Europe/Gibraltar' AS timestamp,
    -- Change NULL values to 0 for numeric columns
    COALESCE(sunshine_minutes_15min, 0) AS sunshine_minutes_15min

FROM raw_sunshine;
