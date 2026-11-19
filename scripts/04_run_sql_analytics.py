import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = "/healthcare-etl-pipeline/healthcare.db"
conn = sqlite3.connect(db_path)

# Query 1: Lead Time vs. No-Show Rate
query_lead_time = '''
SELECT
	CASE
		WHEN a.lead_time_days = 0 THEN '00. Same Day'
		WHEN a.lead_time_days BETWEEN 1 AND 3 THEN '01. 1-3 Days'
		WHEN a.lead_time_days BETWEEN 4 AND 7 THEN '02. 4-7 Days'
		WHEN a.lead_time_days BETWEEN 8 AND 14 THEN '03. 8-14 Days'
		ELSE '04. 15+ Days'
	END AS lead_time_bucket,
	COUNT(*) AS total_appointments,
	SUM(a.no_show_flag) AS total_no_shows,
	ROUND(AVG(a.no_show_flag) * 100.0, 2) AS no_show_rate_pct
FROM fact_appointment a
JOIN dim_patient p ON a.patient_id = p.patient_id
GROUP BY lead_time_bucket
ORDER BY lead_time_bucket;
'''

df_lead_time = pd.read_sql(query_lead_time, conn)
print(df_lead_time)

# Export Query 1 results
output_csv_1 = "/healthcare-etl-pipeline/data/processed/kpi_lead_time_summary.csv"
df_lead_time.to_csv(output_csv_1, index=False)
print(f"Saved Query 1 results to {output_csv_1}\n")

# Query 2: Appointment Sequence via Window Function (CTE)
query_visit_sequence = '''
WITH ranked_appointments AS (
	SELECT
		appointment_id,
		patient_id,
		appointment_day,
		no_show_flag,
		ROW_NUMBER() OVER (
			PARTITION BY patient_id
			ORDER BY appointment_day, appointment_id
		) AS visit_number
	FROM fact_appointment
)

SELECT
	CASE
		WHEN visit_number = 1 THEN '1st Visit'
		WHEN visit_number = 2 THEN '2nd Visit'
		WHEN visit_number = 3 THEN '3rd Visit'
		ELSE '4th+ Visit'
	END AS visit_sequence,
	COUNT(*) AS total_appointments,
	SUM(no_show_flag) AS total_no_shows,
	ROUND(AVG(no_show_flag) * 100.0, 2) AS no_show_rate_pct
FROM ranked_appointments
GROUP BY visit_sequence
ORDER BY visit_sequence;
'''

df_visit_sequence = pd.read_sql(query_visit_sequence, conn)
print(df_visit_sequence)

# Export Query 2 results
output_csv_2 = "/healthcare-etl-pipeline/data/processed/kpi_visit_sequence_summary.csv"
df_visit_sequence.to_csv(output_csv_2, index=False)
print(f"Saved Query 2 results to {output_csv_2}\n")

conn.close()
