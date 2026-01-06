import shutil
import os
import subprocess
import time

# Limpiar carpetas
for folder in ['build', 'dist']:
    if os.path.exists(folder):
        print(f"Borrando {folder}...")
        try:
            shutil.rmtree(folder)
        except Exception as e:
            print(f"Error borrando {folder}: {e}. Intentando forzar...")
            time.sleep(1)
            try:
                shutil.rmtree(folder)
            except:
                print("No se pudo borrar. Continuamos igual.")

print("Iniciando PyInstaller...")
subprocess.run(['pyinstaller', '--clean', 'Verbum Atlas 2026.spec'], check=True)
print("¡Compilación terminada!")
