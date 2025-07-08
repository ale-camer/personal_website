@echo off
REM =============================================================================
REM ==               Script de configuración de proyecto v5.0                  ==
REM ==     Soluciona el problema de expansión de variables con "Delayed Expansion"     ==
REM =============================================================================

REM Habilita la Expansión Retrasada. Esencial para leer variables dentro de bloques.
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set TOOLS_REQ_FILE=%SCRIPT_DIR%tools-requirements.txt
set TEMP_DEPS_FILE=%SCRIPT_DIR%temp_deps.txt

echo.
echo [PASO 1 de 5] Verificando la instalacion de Python...
python --version >nul 2>&1 || (echo [ERROR] Python no encontrado. & pause & exit /b 1)
echo Python encontrado.

echo.
echo [PASO 2 de 5] Limpiando y creando un nuevo entorno virtual 'venv'...
if exist venv ( rmdir /s /q venv )
python -m venv venv || (echo [ERROR] No se pudo crear el entorno virtual. & pause & exit /b 1)

echo.
echo [PASO 3 de 5] Activando entorno e instalando dependencias...
call venv\Scripts\activate.bat

echo Entorno activado.
if exist "%TOOLS_REQ_FILE%" (
    echo Instalando herramientas de desarrollo...
    pip install -r "%TOOLS_REQ_FILE%" --quiet || (echo [ERROR] Fallo al instalar herramientas. & pause & exit /b 1)
)

echo Descubriendo dependencias del proyecto...
python modules/generate_requirements.py --discover

if not exist "%TEMP_DEPS_FILE%" (
    echo [INFO] No se descubrieron dependencias del proyecto para instalar.
) else (
    REM Leemos el contenido del archivo en la variable
    FOR /F "usebackq tokens=*" %%i IN ("%TEMP_DEPS_FILE%") DO SET "PACKAGES_TO_INSTALL=%%i"
    
    echo Instalando dependencias del proyecto...
    REM Usamos !VARIABLES! en lugar de %VARIABLES% para la expansión retrasada
    pip install !PACKAGES_TO_INSTALL! || (echo [ERROR] Fallo al instalar las dependencias del proyecto. & pause & exit /b 1)
    
    del "%TEMP_DEPS_FILE%"
)

echo.
echo [PASO 4 de 5] Generando el archivo 'requirements.txt' final...
python modules/generate_requirements.py || (echo [ERROR] Fallo al generar el 'requirements.txt' final. & pause & exit /b 1)

echo.
echo [PASO 5 de 5] Proceso completado.
echo ----------------------------------------------------------------
echo.
echo  PROYECTO LISTO Y CONFIGURADO
echo.
echo   - Entorno virtual creado en 'venv'.
echo   - Dependencias instaladas.
echo   - 'requirements.txt' generado con versiones.
echo.
echo   Para empezar, activa el entorno: .\venv\Scripts\activate
echo.
echo ----------------------------------------------------------------

pause
endlocal