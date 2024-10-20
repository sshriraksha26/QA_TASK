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

# Initialize session state to hold the tasks data
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Set the title
st.title("QA Daily Task Update")

# Create a form for daily task updates
with st.form(key='qa_update_form'):
    serial_number = st.number_input("Serial Number", min_value=1)
    date = st.date_input("Date", datetime.today())
    tester_name = st.text_input("Tester Name")
    task_name = st.text_input("Task Name")
    jira_created_count = st.number_input("Jira Created Count", min_value=0)
    jira_regressed_count = st.number_input("Jira Regressed Count", min_value=0)

    # Dropdown for Test Case Execution Status
    status_options = ["Completed", "In Progress", "Blocked"]
    execution_status = st.selectbox("Test Case Execution Status", status_options)

    time_spent = st.number_input("Time Spent (hours)", min_value=0.0, format="%.2f")
    comments = st.text_area("Comments")

    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Collect data in a dictionary
        data = {
            "Serial Number": serial_number,
            "Date": date,
            "Tester Name": tester_name,
            "Task Name": task_name,
            "Jira Created Count": jira_created_count,
            "Jira Regressed Count": jira_regressed_count,
            "Execution Status": execution_status,
            "Time Spent": time_spent,
            "Comments": comments
        }

        # Append data to the session state
        st.session_state.tasks.append(data)
        st.success("Task updated successfully!")

# Display all tasks in a table format
if st.session_state.tasks:
    tasks_df = pd.DataFrame(st.session_state.tasks)


    # Function to edit a task
    def edit_task(index):
        task = tasks_df.iloc[index]
        serial_number = st.number_input("Serial Number", value=task['Serial Number'], min_value=1)
        date = st.date_input("Date", value=task['Date'])
        tester_name = st.text_input("Tester Name", value=task['Tester Name'])
        task_name = st.text_input("Task Name", value=task['Task Name'])
        jira_created_count = st.number_input("Jira Created Count", value=task['Jira Created Count'], min_value=0)
        jira_regressed_count = st.number_input("Jira Regressed Count", value=task['Jira Regressed Count'], min_value=0)
        execution_status = st.selectbox("Test Case Execution Status", status_options,
                                        index=status_options.index(task['Execution Status']))
        time_spent = st.number_input("Time Spent (hours)", value=task['Time Spent'], min_value=0.0, format="%.2f")
        comments = st.text_area("Comments", value=task['Comments'])

        if st.button("Update Task"):
            st.session_state.tasks[index] = {
                "Serial Number": serial_number,
                "Date": date,
                "Tester Name": tester_name,
                "Task Name": task_name,
                "Jira Created Count": jira_created_count,
                "Jira Regressed Count": jira_regressed_count,
                "Execution Status": execution_status,
                "Time Spent": time_spent,
                "Comments": comments
            }
            st.success("Task updated successfully!")


    # Function to delete a task
    def delete_task(index):
        del st.session_state.tasks[index]
        st.success("Task deleted successfully!")


    for index, row in tasks_df.iterrows():
        st.write(f"### Task {index + 1}")
        st.write(row)

        edit_button = st.button("Edit", key=f"edit_{index}")
        delete_button = st.button("Delete", key=f"delete_{index}")

        if edit_button:
            edit_task(index)

        if delete_button:
            delete_task(index)

    # Display the updated tasks DataFrame
    st.dataframe(tasks_df)
