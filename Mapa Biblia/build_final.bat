@echo off
echo Limpiando builds anteriores...
rmdir /s /q build
rmdir /s /q dist

echo Construyendo Ejecutable Verbum Atlas v3.1 (Mormón Edition)...
pyinstaller --clean "Verbum Atlas 2026.spec"

echo.
echo ==========================================
echo    COMPILACIÓN TERMINADA
echo ==========================================
if exist "dist\Verbum Atlas 2026\Verbum Atlas 2026.exe" (
    echo [EXITO] El ejecutable se creó correctamente.
    echo Ruta: dist\Verbum Atlas 2026\Verbum Atlas 2026.exe
) else (
    echo [ERROR] No se encontró el ejecutable.
)
pause
