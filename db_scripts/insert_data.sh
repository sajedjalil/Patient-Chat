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
    psql -d $DB_NAME -c "SELECT * FROM patient;" -P pager=off

    echo "Displaying inserted chat history data:"
    psql -d $DB_NAME -c "SELECT * FROM chat_history;" -P pager=off
else
    echo "Failed to insert sample data."
fi