/*
----------------------------------------------------------------------
International Organization for Standardization (ISO) Database Schema
----------------------------------------------------------------------
This script is a customized database for geographic information for
the global standards for trusted goods and services. ISO is an
independent, non-governmental international organization. It brings
global experts together to agree on the best ways of doing things.

Procured by Jason Monroe (jason@jasonmonroe.com)

Note: Storing latitude and longitude coordinates for the Haversine
Formula.

@link https://www.iso.org/home.html
@link https://www.iso.org/obp/ui/#search
@link https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
@link https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
@link https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
@link https://www.timeanddate.com/time/zones/
*/

CREATE DATABASE IF NOT EXISTS iso
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE iso;

CREATE TABLE location (
    id MEDIUMINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    coordinates POINT NOT NULL SRID 4326, -- used for Geographic Information System
    SPATIAL INDEX(coordinates),  -- Enables efficient spatial queries
    latitude DECIMAL(10wd, 8), -- used for Haversine Formula (North to South)
    longitude DECIMAL(11, 8), -- used for Haversine Formula (East to West)
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

-- @link https://mkyong.com/java8/java-display-all-zoneid-and-its-utc-offset/
CREATE TABLE timezone (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    standard_time_name VARCHAR(64) NOT NULL, -- i.e: Central Standard Time
    name VARCHAR(32) UNIQUE NOT NULL, -- i.e: America/Chicago
    alpha_2_code CHAR(2),
    offset VARCHAR(16), -- i.e: UTC+12:00
    group_offset BOOLEAN DEFAULT FALSE, -- used to group timezones by offset to prevent displaying all timezones
    ordering INT UNSIGNED, -- order by offset
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
    );

-- ISO 639
CREATE TABLE language (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    name VARCHAR(32) UNIQUE NOT NULL,
    local_name VARCHAR(32), -- name in local language
    alpha_2_code CHAR(2) UNIQUE NOT NULL, -- iso code 2 chars
    alpha_3_code CHAR(3) UNIQUE NOT NULL, -- iso code 3 chars
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

-- ISO 4217
-- @link https://www.iso.org/iso-4217-currency-codes.html
CREATE TABLE currency (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL, -- i.e: United States Dollar
    iso_code VARCHAR(3) UNIQUE NOT NULL, -- i.e: USD
    symbol VARCHAR(4) NOT NULL, -- i.e: $
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

--  ISO 3166-1
CREATE TABLE country (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    long_name VARCHAR(128) UNIQUE NOT NULL,
    local_name VARCHAR(64) UNIQUE,
    alpha_2_code CHAR(2) UNIQUE NOT NULL, -- iso code 2 chars
    alpha_3_code CHAR(3) UNIQUE NOT NULL, -- iso code 3 chars
    numeric_code INT(3) UNIQUE , -- ie: 840
    capital VARCHAR(64), -- optional
    capital_id INT UNSIGNED,
    nationality_plural VARCHAR(64),
    nationality_singular VARCHAR(64),
    continent VARCHAR(16), -- i.e: Africa, Europe, North America, South America, Oceania, Asia, Middle East, Caribbean
    flag_emoji VARCHAR(2) UNIQUE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, -- emoji icon
    currency_id INT UNSIGNED,
    location_id INT UNSIGNED, -- if normalized
    coordinates POINT NOT NULL SRID 4326, -- used for Geographic Information System (GIS)
    SPATIAL INDEX(coordinates),  -- enables efficient spatial queries
    latitude DECIMAL(10, 8), -- used for Haversine Formula
    longitude DECIMAL(11, 8), -- used for Haversine Formula
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    FOREIGN KEY (location_id) REFERENCES location(id) ON UPDATE CASCADE ON DELETE CASCADE
    FOREIGN KEY (capital_id) REFERENCES city(id) ON UPDATE CASCADE ON DELETE SET NULL
    FOREIGN KEY (currency_id) REFERENCES currency(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- ISO 33166-2
CREATE TABLE region (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    country_id SMALLINT UNSIGNED NOT NULL,
    location_id MEDIUMINT UNSIGNED,
    language_id SMALLINT UNSIGNED,
    name VARCHAR(64) UNIQUE NOT NULL,
    iso_code VARCHAR(8) UNIQUE NOT NULL, -- 3166-2 iso sub-division code
    coordinates POINT NOT NULL SRID 4326, -- used for Geographic Information System
    SPATIAL INDEX(coordinates), -- enables efficient spatial queries
    latitude DECIMAL(10, 8), -- used for Haversine Formula
    longitude DECIMAL(11, 8), -- used for Haversine Formula
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    FOREIGN KEY (country_id) REFERENCES country(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES language(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Metropolitan area
-- Used to bundle cities of a suburban areas to a metropolitan area
CREATE TABLE metro (
    id SMALLINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    city_id INT, -- used as a REFERENCES to the city proper of the metro (optional)
    name VARCHAR(64) UNIQUE NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

-- cities
-- @link https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/sql/cities.sql
CREATE TABLE city (
    id MEDIUMINT UNSIGNED UNIQUE NOT NULL AUTO_INCREMENT,
    region_id SMALLINT UNSIGNED NOT NULL,
    metro_id SMALLINT UNSIGNED,
    timezone_id SMALLINT UNSIGNED,
    location_id MEDIUMINT UNSIGNED,
    name VARCHAR(64) UNIQUE NOT NULL,
    coordinates POINT NOT NULL SRID 4326, -- used for Geographic Information System
    SPATIAL INDEX(coordinates),  -- Enables efficient spatial queries
    latitude DECIMAL(10, 8), -- used for Haversine Formula
    longitude DECIMAL(11, 8), -- used for Haversine Formula
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    FOREIGN KEY (region_id) REFERENCES region(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (metro_id) REFERENCES location(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (timezone_id) REFERENCES timezone(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- CREATE indices on foreign keys, UNIQUE and joined columns

-- Indices: location
CREATE SPATIAL INDEX idx_location_coordinates ON location(coordinates);
CREATE INDEX idx_location_lon ON location(longitude);
CREATE INDEX idx_location_lat ON location(latitude);
CREATE INDEX idx_location_tz ON location(timezone_id);

-- Indices: timezone
CREATE INDEX idx_tz_name ON timezone(name);
CREATE INDEX idx_tz_iso_code ON timezone(alpha_2_code);
CREATE INDEX idx_tz_group_offset ON timezone(group_offset);
CREATE INDEX idx_tz_standard_name ON timezone(standard_time_name);

-- Indices: language
CREATE INDEX idx_language_name ON language(name);
CREATE INDEX idx_language_local_name ON language(local_name);
CREATE INDEX idx_language_alpha_2_code ON language(alpha_2_code);
CREATE INDEX idx_language_alpha_3_code ON language(alpha_3_code);

-- Indices: country
CREATE INDEX idx_country_name ON country(name);
CREATE INDEX idx_country_long_name ON country(long_name);
CREATE INDEX idx_country_local_name ON country(local_name);
CREATE INDEX idx_country_numeric_code ON country(numeric_code);
CREATE INDEX idx_country_location ON country(location_id);
CREATE INDEX idx_country_capital ON country(capital_id);
CREATE INDEX idx_country_currency ON currency(id);
CREATE INDEX idx_country_query ON country(name, location_id, alpha_2_code);
CREATE SPATIAL INDEX idx_country_coordinates ON country(coordinates);
CREATE INDEX idx_country_lon ON country(longitude);
CREATE INDEX idx_country_lat ON country(latitude);

-- Indices: region
CREATE INDEX idx_region_country ON region(country_id);
CREATE INDEX idx_region_language ON region(language_id);
CREATE INDEX idx_region_name ON region(name);
CREATE INDEX idx_region_iso_code ON region(iso_code);
CREATE INDEX idx_region_location ON region(location_id);
CREATE INDEX idx_region_query ON region(country_id, location_id, name);
CREATE SPATIAL INDEX idx_region_coordinates ON region(coordinates);
CREATE INDEX idx_region_lon ON region(longitude);
CREATE INDEX idx_region_lat ON region(latitude);

-- Indices: metro
CREATE INDEX idx_metro_city ON metro(city_id);
CREATE INDEX idx_metro_name ON metro(name);

-- Indices: city
CREATE INDEX idx_city_region ON city(region_id);
CREATE INDEX idx_city_metro ON city(metro_id);
CREATE INDEX idx_city_timezone ON city(timezone_id);
CREATE INDEX idx_city_location ON city(location_id);
CREATE INDEX idx_city_name ON city(name);
CREATE INDEX idx_city_query ON city(region_id, location_id, name, metro_id);
CREATE SPATIAL INDEX idx_city_coordinates ON city(coordinates);
CREATE INDEX idx_city_lon ON city(longitude);
CREATE INDEX idx_city_lat ON city(latitude);
