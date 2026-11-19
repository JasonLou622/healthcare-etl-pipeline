# Database Design & Loading
import sqlite3
import pandas as pd

# 1. Connect to local SQLite database (creates healthcare.db if it doesn't exist)
db_path = "/healthcare-etl-pipeline/healthcare.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. Read processed CSV
csv_path = "/healthcare-etl-pipeline/data/processed/cleaned_appointments.csv"
df = pd.read_csv(csv_path)

# 3. Create relational schema
# dim_patient: static demographic info
cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_patient (
	patient_id INTEGER PRIMARY KEY,
	gender TEXT,
	age INTEGER
);
''')

# fact_appointment: transactional records
cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_appointment (
	appointment_id INTEGER PRIMARY KEY,
	patient_id INTEGER,
	scheduled_day TEXT,
	appointement_day TEXT,
	neighbourhood TEXT,
	scholarship INTEGER,
	hypertension INTEGER,
	diabetes INTEGER,
	alcoholism INTEGER,
	handicap INTEGER,
	sms_received INTEGER,
	lead_time_days INTEGER,
	no_show_flag INTEGER,
	FOREIGN KEY (patient_id) REFERENCES dim_patient (patient_id)
);
''')
conn.commit()

# 4. Populate dim_patient (deduplicate patients by patient_id)
dim_patient_df = df[['patient_id', 'gender', 'age']].drop_duplicates(subset=['patient_id'])
dim_patient_df.to_sql('dim_patient', conn, if_exists='replace', index=False)

# 5. Populate fact_appointment
fact_cols = [
	'appointment_id', 'patient_id', 'scheduled_day', 'appointment_day',
	'neighbourhood', 'scholarship', 'hypertension', 'diabetes',
	'alcoholism', 'handicap', 'sms_received', 'lead_time_days', 'no_show_flag'
]
df[fact_cols].to_sql('fact_appointment', conn, if_exists='replace', index=False)

# 6. Verify row insertion counts
patient_count = cursor.execute("SELECT COUNT(*) FROM dim_patient;").fetchone()[0]
appointment_count = cursor.execute("SELECT COUNT(*) FROM fact_appointment;").fetchone()[0]

print(f"Database successfully loaded:")
print(f"- Total unique patients in dim_patient: {patient_count}")
print(f"- Total encounters in fact_appointment: {appointment_count}")

conn.close()

