# build.ps1
Write-Host "=== Iniciando compilación de utilidades FFmpeg en ./dist ===" -ForegroundColor Cyan

# 1. Limpieza inicial de temporales
Write-Host "Limpiando archivos temporales..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

$specs = @("trimmer.spec", "compressor.spec", "union.spec")
foreach ($spec in $specs) {
    if (Test-Path $spec) { Remove-Item -Force $spec }
}

# 2. Compilar cada script
$scripts = @("trimmer.py", "compressor.py", "union.py")

foreach ($script in $scripts) {
    Write-Host "Empaquetando $script..." -ForegroundColor Yellow
    pyinstaller --onefile --collect-all ffmpeg $script

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al compilar $script." -ForegroundColor Red
    }
}

# 3. Limpieza de artefactos post-compilacion
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
foreach ($spec in $specs) {
    if (Test-Path $spec) { Remove-Item -Force $spec }
}

Write-Host "=== ¡Proceso completado! Los ejecutables están listos en la carpeta ./dist ===" -ForegroundColor Green
Get-ChildItem -Path "dist"