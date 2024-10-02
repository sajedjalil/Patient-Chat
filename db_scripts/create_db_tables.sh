#!/bin/bash

DB_NAME="patient_db"

create_db() {
    if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo "Database $DB_NAME already exists."
    else
        psql -d postgres -c "CREATE DATABASE $DB_NAME;"
        echo "Database $DB_NAME created successfully."
    fi
}

create_table() {
    table_name=$(echo "$1" | sed -n 's/.*CREATE TABLE IF NOT EXISTS \([^ ]*\).*/\1/p')
    if psql -d $DB_NAME -c "\d $table_name" &>/dev/null; then
        echo "Table $table_name already exists."
    else
        psql -d $DB_NAME -c "$1"
        echo "Table $table_name created successfully."
    fi
}

# Create database
create_db

# Create patient table
patient_table="
CREATE TABLE IF NOT EXISTS patient (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    medical_conditions TEXT,
    medication_regimen TEXT,
    last_appointment TIMESTAMP,
    next_appointment TIMESTAMP,
    doctor_name VARCHAR(100)
);"
create_table "$patient_table"

# Create chat_history table
chat_history_table="
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patient(id),
    thread_id VARCHAR(50) NOT NULL,
    is_user BOOLEAN NOT NULL,
    text TEXT NOT NULL,
    summary TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"
create_table "$chat_history_table"

echo "Database setup completed."