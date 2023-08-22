@echo off

rem Cambia al directorio del proyecto
cd C:\Users\stecnico\Documents\GitHub\reports_pdf_stored_procedure

rem Activa el entorno virtual
call venv\Scripts\activate.bat

rem Ejecuta el script de Python
python main.py

rem Desactiva el entorno virtual
deactivate

rem Pausa el script para mantener la ventana abierta (opcional)
pause
