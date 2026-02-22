-- dim_weather.sql

-- Drop the table if it already exists to allow for re-runs
DROP TABLE IF EXISTS dim_weather;

-- Create the dimension table from cleaned_sunshine
CREATE TABLE dim_weather (
    weather_key INT PRIMARY KEY,
    condition_name VARCHAR(50) NOT NULL, -- Lesbarer Name
    min_sunshine_min DECIMAL(4,2),       -- Untergrenze in Minuten
    max_sunshine_min DECIMAL(4,2),       -- Obergrenze in Minuten
    is_sunny_threshold BOOLEAN,          -- Flag für "Sonniger Zeitraum"
    description TEXT                     -- Optionale Details
);

INSERT INTO dim_weather (weather_key, condition_name, min_sunshine_min, max_sunshine_min, is_sunny_threshold, description)
VALUES 
    (1, 'Schatten', 0.00, 2.00, FALSE, 'Weniger als 2 Min. Sonne pro Intervall'),
    (2, 'Wolkig', 2.01, 7.50, FALSE, 'Zwischen 2 und 7,5 Min. Sonne'),
    (3, 'Heiter', 7.51, 12.00, TRUE, 'Mehr als 50% Sonnenschein im Intervall'),
    (4, 'Vollsonnig', 12.01, 15.00, TRUE, 'Nahezu ununterbrochener Sonnenschein'),
    (-1, 'Unbekannt', NULL, NULL, FALSE, 'Keine Wetterdaten');
