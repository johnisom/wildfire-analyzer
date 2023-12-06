--sqlite stuff
-- .import --csv --skip 1 fips_codes.csv fips_codes
-- .import --csv --skip 1 fires.csv fires
--end sqlite stuff

--check for "<null>" to replace with NULL

SELECT
  SUM(CASE WHEN id = '<null>' THEN 1 ELSE 0 END) AS id_null_count,
  SUM(CASE WHEN source_system_type = '<null>' THEN 1 ELSE 0 END) AS source_system_type_null_count,
  SUM(CASE WHEN source_system = '<null>' THEN 1 ELSE 0 END) AS source_system_null_count,
  SUM(CASE WHEN source_reporting_unit = '<null>' THEN 1 ELSE 0 END) AS source_reporting_unit_null_count,
  SUM(CASE WHEN source_reporting_unit_name = '<null>' THEN 1 ELSE 0 END) AS source_reporting_unit_name_null_count,
  SUM(CASE WHEN nwcg_reporting_agency = '<null>' THEN 1 ELSE 0 END) AS nwcg_reporting_agency_null_count,
  SUM(CASE WHEN nwcg_reporting_unit_id = '<null>' THEN 1 ELSE 0 END) AS nwcg_reporting_unit_id_null_count,
  SUM(CASE WHEN nwcg_reporting_unit_name = '<null>' THEN 1 ELSE 0 END) AS nwcg_reporting_unit_name_null_count,
  SUM(CASE WHEN local_fire_report_id = '<null>' THEN 1 ELSE 0 END) AS local_fire_report_id_null_count,
  SUM(CASE WHEN local_incident_id = '<null>' THEN 1 ELSE 0 END) AS local_incident_id_null_count,
  SUM(CASE WHEN owner_code = '<null>' THEN 1 ELSE 0 END) AS owner_code_null_count,
  SUM(CASE WHEN owner_descr = '<null>' THEN 1 ELSE 0 END) AS owner_descr_null_count,
  SUM(CASE WHEN fire_code = '<null>' THEN 1 ELSE 0 END) AS fire_code_null_count,
  SUM(CASE WHEN fire_name = '<null>' THEN 1 ELSE 0 END) AS fire_name_null_count,
  SUM(CASE WHEN fire_year = '<null>' THEN 1 ELSE 0 END) AS fire_year_null_count,
  SUM(CASE WHEN discovery_datetime = '<null>' THEN 1 ELSE 0 END) AS discovery_datetime_null_count,
  SUM(CASE WHEN contained_datetime = '<null>' THEN 1 ELSE 0 END) AS contained_datetime_null_count,
  SUM(CASE WHEN stat_cause_code = '<null>' THEN 1 ELSE 0 END) AS stat_cause_code_null_count,
  SUM(CASE WHEN stat_cause_descr = '<null>' THEN 1 ELSE 0 END) AS stat_cause_descr_null_count,
  SUM(CASE WHEN fire_size = '<null>' THEN 1 ELSE 0 END) AS fire_size_null_count,
  SUM(CASE WHEN fire_size_class = '<null>' THEN 1 ELSE 0 END) AS fire_size_class_null_count,
  SUM(CASE WHEN longitude = '<null>' THEN 1 ELSE 0 END) AS longitude_null_count,
  SUM(CASE WHEN latitude = '<null>' THEN 1 ELSE 0 END) AS latitude_null_count,
  SUM(CASE WHEN state_name = '<null>' THEN 1 ELSE 0 END) AS state_name_null_count,
  SUM(CASE WHEN state_alpha_code = '<null>' THEN 1 ELSE 0 END) AS state_alpha_code_null_count,
  SUM(CASE WHEN state_fips_code = '<null>' THEN 1 ELSE 0 END) AS state_fips_code_null_count,
  SUM(CASE WHEN county_name = '<null>' THEN 1 ELSE 0 END) AS county_name_null_count,
  SUM(CASE WHEN county_fips_name = '<null>' THEN 1 ELSE 0 END) AS county_fips_name_null_count,
  SUM(CASE WHEN county_fips_code = '<null>' THEN 1 ELSE 0 END) AS county_fips_code_null_count,
  SUM(CASE WHEN combined_fips_code = '<null>' THEN 1 ELSE 0 END) AS combined_fips_code_null_count
FROM fires;

-- then, for each column with value "<null>", run (replacing **colname** with the actual column name):
-- UPDATE fires SET **colname** = NULL WHERE **colname** = '<null>';