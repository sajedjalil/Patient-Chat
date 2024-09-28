#!/bin/bash

# Database name
DB_NAME="patient_db"

# Create the database
psql -d postgres -c "CREATE DATABASE $DB_NAME;"

# Check if the database was created successfully
if [ $? -ne 0 ]; then
    echo "Failed to create database $DB_NAME"
fi

# Create the patient table
psql -d $DB_NAME -c "
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

# Check if the patient table was created successfully
if [ $? -ne 0 ]; then
    echo "Failed to create table 'patient' in database $DB_NAME"
    exit 1
fi

# Create the chat_history table with modified is_user field
psql -d $DB_NAME -c "
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    is_user BOOLEAN NOT NULL,
    text TEXT NOT NULL,
    summary TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);"

# Check if the chat_history table was created successfully
if [ $? -ne 0 ]; then
    echo "Failed to create table 'chat_history' in database $DB_NAME"
    exit 1
fi

echo "Database $DB_NAME and tables 'patient' and 'chat_history' have been created successfully."