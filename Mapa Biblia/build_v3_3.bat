@echo off
echo Cancelando compilaciones anteriores...
taskkill /F /IM pyinstaller.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1

echo Limpiando carpetas temp...
rmdir /s /q build_final_ok
rmdir /s /q dist_final_ok

echo Iniciando COMPILACIÓN V3.3 (Definitiva)...
pyinstaller --noconfirm --workpath build_final_ok --distpath dist_final_ok "Verbum Atlas 2026.spec"

echo.
echo [INFO] Compilación terminada. Revisa la carpeta dist_final_ok.
pause
