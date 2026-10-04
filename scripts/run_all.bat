@echo off
cd /d "%~dp0.."
python src\main.py --vfs vfs\minimal.csv --prompt "my_vfs> " --script scripts\start.txt
