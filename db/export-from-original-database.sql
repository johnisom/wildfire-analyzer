--sqlite stuff
-- .mode csv
-- .header on
-- .output fires.csv
--end sqlite stuff

SELECT
  OBJECTID AS id,
  SOURCE_SYSTEM_TYPE AS source_system_type,
  SOURCE_SYSTEM AS source_system,
  SOURCE_REPORTING_UNIT AS source_reporting_unit,
  SOURCE_REPORTING_UNIT_NAME AS source_reporting_unit_name,
  NWCG_REPORTING_AGENCY AS nwcg_reporting_agency,
  NWCG_REPORTING_UNIT_ID AS nwcg_reporting_unit_id,
  NWCG_REPORTING_UNIT_NAME AS nwcg_reporting_unit_name,
  LOCAL_FIRE_REPORT_ID AS local_fire_report_id,
  LOCAL_INCIDENT_ID AS local_incident_id,
  CAST(OWNER_CODE AS INTEGER) AS owner_code,
  OWNER_DESCR AS owner_descr,
  FIRE_CODE AS fire_code,
  FIRE_NAME AS fire_name,
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