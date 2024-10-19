import os

# Function to create the batch file
def create_batch_file():
    batch_content = """@echo off
cd /d "%~dp0"
call .venv\\Scripts\\activate  # Activate your virtual environment if needed
streamlit run qa_tracker.py
pause  # Keep the window open after the app exits
"""
    with open('run_app.bat', 'w') as batch_file:
        batch_file.write(batch_content)

# Check if the batch file already exists
if not os.path.exists('run_app.bat'):
    create_batch_file()

import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize a session state to store the data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Serial No', 'Date', 'Employee Name', 'JIRA Logged', 'JIRA Closed',
        'Test Cases Passed', 'Test Cases Failed', 'Test Cases NA',
        'Test Cases Blocked', 'Test Cases Hold'
    ])

# Function to add data
# Function to add data
def add_data(serial_no, date, emp_name, jira_logged, jira_closed, pass_count, fail_count, na_count, blocked_count,
             hold_count):
    new_row = pd.DataFrame({
        'Serial No': [serial_no],
        'Date': [date],
        'Employee Name': [emp_name],
        'JIRA Logged': [jira_logged],
        'JIRA Closed': [jira_closed],
        'Test Cases Passed': [pass_count],
        'Test Cases Failed': [fail_count],
        'Test Cases NA': [na_count],
        'Test Cases Blocked': [blocked_count],
        'Test Cases Hold': [hold_count]
    })

    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)


# Title of the app
st.title("QA Work Status Tracker")

# Input fields for data
serial_no = st.number_input("Serial No", min_value=1, value=1)
date = st.date_input("Date", value=datetime.now())
employee_name = st.text_input("Employee Name")
jira_logged = st.number_input("JIRA Logged", min_value=0)
jira_closed = st.number_input("JIRA Closed", min_value=0)
test_cases_passed = st.number_input("Test Cases Passed", min_value=0)
test_cases_failed = st.number_input("Test Cases Failed", min_value=0)
test_cases_na = st.number_input("Test Cases NA", min_value=0)
test_cases_blocked = st.number_input("Test Cases Blocked", min_value=0)
test_cases_hold = st.number_input("Test Cases Hold", min_value=0)

# Button to submit data
if st.button("Submit"):
    add_data(serial_no, date, employee_name, jira_logged, jira_closed,
              test_cases_passed, test_cases_failed, test_cases_na,
              test_cases_blocked, test_cases_hold)
    st.success("Data added successfully!")

# Display the data
st.subheader("QA Work Status Data")
st.dataframe(st.session_state.data)

# Optionally, you can add a download button for the data
if st.button("Download Data as CSV"):
    csv = st.session_state.data.to_csv(index=False)
    st.download_button("Download CSV", csv, "qa_work_status.csv", "text/csv")
