--sqlite stuff
-- .mode csv
-- .header on
-- .output fires.csv
--end sqlite stuff

SELECT
  OBJECTID AS id,
  FIRE_YEAR AS fire_year,
  CAST(CASE WHEN DISCOVERY_TIME IS NULL THEN STRFTIME('%s', DATETIME(DISCOVERY_DATE)) ELSE STRFTIME('%s', DATETIME(DISCOVERY_DATE, CAST(CAST(DISCOVERY_TIME AS integer)/100 AS STRING) || ' hours', CAST(CAST(DISCOVERY_TIME AS integer)%100 AS STRING) || ' minutes')) END AS INTEGER) AS discovery_datetime,
  CAST(CASE WHEN CONT_TIME IS NULL THEN STRFTIME('%s', DATETIME(CONT_DATE)) ELSE STRFTIME('%s', DATETIME(CONT_DATE, CAST(CAST(CONT_TIME AS integer)/100 AS STRING) || ' hours', CAST(CAST(CONT_TIME AS integer) %100 AS STRING) || ' minutes')) END AS INTEGER) AS contained_datetime,
  CAST(STAT_CAUSE_CODE AS INTEGER) AS stat_cause_code,
  STAT_CAUSE_DESCR AS stat_cause_descr,
  FIRE_SIZE AS fire_size,
  FIRE_SIZE_CLASS AS fire_size_class,
  LONGITUDE AS longitude,
  LATITUDE AS latitude,
  NULL AS state_name,
  STATE AS state_alpha_code,
  NULL AS state_fips_code,
  NULL as county_name,
  FIPS_NAME AS county_fips_name,
  FIPS_CODE AS county_fips_code,
  NULL AS combined_fips_code
FROM Fires;

--sqlite stuff
-- .output
-- .exit
--end sqlite stuff