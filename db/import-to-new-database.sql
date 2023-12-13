--sqlite stuff
-- .import --csv --skip 1 fips_codes.csv fips_codes
-- .import --csv --skip 1 fires.csv fires
--end sqlite stuff

--check for "<null>" to replace with NULL

SELECT
  SUM(CASE WHEN id is NULL THEN 1 ELSE 0 END) AS id_null_count,
  SUM(CASE WHEN fire_year is NULL THEN 1 ELSE 0 END) AS fire_year_null_count,
  SUM(CASE WHEN discovery_datetime is NULL THEN 1 ELSE 0 END) AS discovery_datetime_null_count,
  SUM(CASE WHEN contained_datetime is NULL THEN 1 ELSE 0 END) AS contained_datetime_null_count,
  SUM(CASE WHEN stat_cause_code is NULL THEN 1 ELSE 0 END) AS stat_cause_code_null_count,
  SUM(CASE WHEN stat_cause_descr is NULL THEN 1 ELSE 0 END) AS stat_cause_descr_null_count,
  SUM(CASE WHEN fire_size is NULL THEN 1 ELSE 0 END) AS fire_size_null_count,
  SUM(CASE WHEN fire_size_class is NULL THEN 1 ELSE 0 END) AS fire_size_class_null_count,
  SUM(CASE WHEN longitude is NULL THEN 1 ELSE 0 END) AS longitude_null_count,
  SUM(CASE WHEN latitude is NULL THEN 1 ELSE 0 END) AS latitude_null_count,
  SUM(CASE WHEN state_name is NULL THEN 1 ELSE 0 END) AS state_name_null_count,
  SUM(CASE WHEN state_alpha_code is NULL THEN 1 ELSE 0 END) AS state_alpha_code_null_count,
  SUM(CASE WHEN state_fips_code is NULL THEN 1 ELSE 0 END) AS state_fips_code_null_count,
  SUM(CASE WHEN county_name is NULL THEN 1 ELSE 0 END) AS county_name_null_count,
  SUM(CASE WHEN county_fips_name is NULL THEN 1 ELSE 0 END) AS county_fips_name_null_count,
  SUM(CASE WHEN county_fips_code is NULL THEN 1 ELSE 0 END) AS county_fips_code_null_count,
  SUM(CASE WHEN combined_fips_code is NULL THEN 1 ELSE 0 END) AS combined_fips_code_null_count
FROM fires;

-- then, for each column with value "<null>", run (replacing **colname** with the actual column name):
-- UPDATE fires SET **colname** = NULL WHERE **colname** = '<null>';