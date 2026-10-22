#!/bin/bash

echo "=== Iniciando compilación de utilidades FFmpeg en ./dist para Linux ==="

# 1. Limpieza inicial
echo "Limpiando archivos temporales..."
rm -rf build dist *.spec

# 2. Compilar cada script
scripts=("trimmer.py" "compressor.py" "union.py")

for script in "${scripts[@]}"; do
    echo "Empaquetando $script..."
    pyinstaller --onefile --collect-all ffmpeg "$script"

    if [ $? -ne 0 ]; then
        echo "Error al compilar $script."
    fi
done

# 3. Limpieza de artefactos post-compilación y permisos
rm -rf build *.spec

if [ -d "dist" ]; then
    chmod +x dist/*
fi

echo "=== ¡Proceso completado! Los binarios están listos en la carpeta ./dist ==="
ls -l dist