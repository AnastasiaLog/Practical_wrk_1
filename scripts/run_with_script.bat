@echo off
cd /d "%~dp0.."
python src\main.py --vfs vfs\few_files.csv --script scripts\start.txt
