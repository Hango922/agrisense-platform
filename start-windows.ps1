$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw 'Create .venv and install requirements.txt first.' }
$env:DJANGO_SETTINGS_MODULE = 'nongsan_project.operational_settings'
& $python manage.py check
if ($LASTEXITCODE -ne 0) { throw 'Django check failed.' }
& $python manage.py check_operations
if ($LASTEXITCODE -ne 0) { throw 'Operator credentials must be fixed before starting.' }
& $python manage.py migrate --check
if ($LASTEXITCODE -ne 0) { throw 'Pending migrations: run manage.py migrate before starting.' }
& $python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) { throw 'Static asset collection failed.' }
Write-Host 'Starting AgriSense on loopback. Press Ctrl+C to stop.'
& $python serve.py
if ($LASTEXITCODE -ne 0) { throw 'Server stopped with an error; check the port and logs.' }
