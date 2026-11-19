-- Query 1: Evaluate No-Show Rate by Scheduling Lead-Time Bracket
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
-- Query 2: Evaluate Repeat Visit Attendance via Window Functions (CTE)
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
