@echo off
REM Runs the compute_urgency white-box tests with branch coverage.
REM Double-click this file. It saves the results in this folder.
cd /d "%~dp0..\.."
call venv\Scripts\activate.bat
python -m pip install --quiet pytest pytest-cov
echo Running tests...
python -m pytest 02_White_Box_Coverage/compute_urgency/tests/test_compute_urgency.py --cov=helpers --cov-branch --cov-report=term-missing --cov-report=html:02_White_Box_Coverage/compute_urgency/htmlcov -v -p no:cacheprovider > 02_White_Box_Coverage\compute_urgency\pytest_output_compute_urgency.txt 2>&1
type 02_White_Box_Coverage\compute_urgency\pytest_output_compute_urgency.txt | findstr /R /C:"PASSED" /C:"FAILED" /C:"^helpers.py" /C:"^Name" /C:"passed"
echo.
echo Full log: 02_White_Box_Coverage\compute_urgency\pytest_output_compute_urgency.txt
echo Coverage report: 02_White_Box_Coverage\compute_urgency\htmlcov\index.html
pause
