[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    $python = Join-Path $projectRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $python)) {
        & py -3 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Install Python 3.11+ and retry." }
    }
    & $python -m pip install -e .
    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
    & $python -m pip check
    if ($LASTEXITCODE -ne 0) { throw "Dependency validation failed." }
    & $python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Tests failed." }
    Write-Host "Ready. Follow docs/USE_NOW.md. No personal data was imported."
} finally {
    Pop-Location
}
