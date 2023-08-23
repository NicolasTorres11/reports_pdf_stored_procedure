@echo off

rem Ruta del programa
set "program_path=C:\Users\stecnico\Documents\GitHub\reports_pdf_stored_procedure\proc_mon"

rem Activa el entorno virtual (ajusta el nombre del entorno si es diferente)
call %program_path%\venv\Scripts\activate

rem Cambia al directorio del programa
cd /d %program_path%

rem Ejecuta tu script Python
python main.py

rem Desactiva el entorno virtual
deactivate
