@echo off
echo Stopping all Python processes to resolve bot conflicts...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul
echo All Python processes stopped.
echo You can now start the bot without conflicts.
pause