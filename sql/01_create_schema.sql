-- Dimension Table: Static patient demographics
CREATE TABLE IF NOT EXISTS dim_patient (
    patient_id INTEGER PRIMARY KEY,
    gender TEXT,
    age INTEGER
);

-- Fact Table: Transactional appointment records
CREATE TABLE IF NOT EXISTS fact_appointment (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    scheduled_day TEXT,
    appointment_day TEXT,
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
