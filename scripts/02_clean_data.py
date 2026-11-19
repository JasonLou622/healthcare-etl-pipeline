import pandas as pd

# 1. Load the raw data
raw_path = "/healthcare-etl-pipeline/data/raw/appointments.csv"
df = pd.read_csv(raw_path)

print("Starting cleaning and Initial count:", len(df))

# 2. Rename columns to consistent snake_case and fix spelling
df = df.rename(columns={
	'PatientId': 'patient_id',
	'AppointmentID': 'appointment_id',
	'Gender': 'gender',
	'ScheduledDay': 'scheduled_day',
	'AppointmentDay': 'appointment_day',
	'Age': 'age',
	'Neighbourhood': 'neighbourhood',
	'Scholarship': 'scholarship',
	'Hipertension': 'hypertension',
	'Diabetes': 'diabetes',
	'Alcoholism': 'alcoholism',
	'Handcap': 'handicap',
	'SMS_received': 'sms_received',
	'No-show': 'no_show'
})

# 3. Standardize IDs
df['patient_id'] = df['patient_id'].astype('int64')

# 4. Parse Dates (strip timestamps to dates for fair lead-time calculation)
df['scheduled_day'] = pd.to_datetime(df['scheduled_day']).dt.date
df['appointment_day'] = pd.to_datetime(df['appointment_day']).dt.date

# 5. Feature Engineering: Lead Time (Wait Days)
df['lead_time_days'] = (pd.to_datetime(df['appointment_day']) - pd.to_datetime(df['scheduled_day'])).dt.days

# 6. Filter Anomalies
# Remove impossible ages (e.g., age < 0 or age > 115)
# Remove negative lead time (appointment day occurring before scheduled day)
df_clean = df[(df['age'] >= 0) & (df['age'] <= 115)].copy()
df_clean = df_clean[df_clean['lead_time_days'] >= 0].copy()

# 7. Standardize binary target: 1 = No-show, 0 = Showed up
df_clean['no_show_flag'] = (df_clean['no_show'] == 'Yes').astype(int)

# 8. Save cleaned dataset
output_path = "/healthcare-etl-pipeline/data/processed/cleaned_appointments.csv"
df_clean.to_csv(output_path, index=False)

print(f"Cleaning complete! Saved {len(df_clean)} rows to {output_path}")
print(df_clean[['age', 'lead_time_days', 'no_show_flag']].describe())

