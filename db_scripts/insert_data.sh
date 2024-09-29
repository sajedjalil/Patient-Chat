#!/bin/bash

# Database name
DB_NAME="patient_db"

# SQL commands to insert sample data
SQL_COMMANDS="
-- Insert sample patient
INSERT INTO patient (
    first_name,
    last_name,
    date_of_birth,
    phone_number,
    email,
    medical_conditions,
    medication_regimen,
    last_appointment,
    next_appointment,
    doctor_name
) VALUES (
    'Nikola',
    'Tesla',
    '07-10-1856',
    '(555) 123-4567',
    'nicktesla@email.com',
    'Hypertension, Type 2 Diabetes',
    'Metformin 500mg twice daily, Lisinopril 10mg once daily',
    '2023-09-15 10:30:00',
    '2024-03-15 14:00:00',
    'Dr. Jane Smith'
) RETURNING id;

-- Insert sample chat history entries
INSERT INTO chat_history (patient_id, thread_id, is_user, text, summary)
VALUES
    (currval('patient_id_seq'), 'ebc92830-6110-45d8-bea9-fead9e51cd17', FALSE, 'Hello, I''ve been experiencing increased thirst lately. Is this related to my diabetes?', 'Patient reports increased thirst'),
    (currval('patient_id_seq'), 'ebc92830-6110-45d8-bea9-fead9e51cd17', TRUE, 'Hi John, increased thirst can indeed be a symptom of diabetes. Let''s schedule a check-up to monitor your blood sugar levels. How does next week look for you?', 'System suggests check-up for diabetes symptoms'),
    (currval('patient_id_seq'), 'nks72743-4565-87s6-idw4-tour3e23we52', FALSE, 'Next week works for me. Should I prepare anything specific for the appointment?', 'Patient agrees to check-up, asks for preparation instructions');
"

# Execute the SQL commands
psql -d $DB_NAME << EOF
$SQL_COMMANDS
EOF

# Check if the insertion was successful
if [ $? -eq 0 ]; then
    echo "Sample data inserted successfully."

    # Display the inserted data
    echo "Displaying inserted patient data:"
    psql -d $DB_NAME -c "SELECT * FROM patient;"

    echo "Displaying inserted chat history data:"
    psql -d $DB_NAME -c "SELECT * FROM chat_history;"
else
    echo "Failed to insert sample data."
fi