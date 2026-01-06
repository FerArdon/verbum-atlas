@echo off
echo ========================================
echo   CONSTRUYENDO VERBUM ATLAS 2026
echo ========================================
echo.
echo 1. Limpiando carpetas temporales...
if exist build rd /s /q build
if exist dist rd /s /q dist

echo.
echo 2. Iniciando PyInstaller...
pyinstaller --noconfirm "Verbum Atlas 2026.spec"

echo.
echo 3. Proceso completado.
echo El ejecutable se encuentra en la carpeta 'dist'.
pause
