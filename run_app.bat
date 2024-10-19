@echo off
cd /d "%~dp0"
call .venv\Scripts\activate  # Activate your virtual environment if needed
streamlit run qa_tracker.py
pause  # Keep the window open after the app exits
