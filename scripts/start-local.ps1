[CmdletBinding()]
param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$dataDirectory = Join-Path $projectRoot ".local"
$databasePath = Join-Path $dataDirectory "openwear-local.db"
$serverExecutable = Join-Path $projectRoot ".venv\Scripts\openwear-coach.exe"

New-Item -ItemType Directory -Force -Path $dataDirectory | Out-Null

if (-not (Test-Path -LiteralPath $serverExecutable -PathType Leaf)) {
    throw "Local environment missing. Create .venv and install the project before starting OpenWear."
}

$env:OPENWEAR_DB = $databasePath
$env:OPENWEAR_HOST = "127.0.0.1"
$env:OPENWEAR_PORT = [string]$Port
$env:OPENWEAR_TRANSPORT = "streamable-http"

Write-Host "OpenWear Coach is local-only: http://127.0.0.1:$Port/mcp"
Write-Host "Database: .local/openwear-local.db (ignored by Git)"
Write-Host "Press Ctrl+C to stop."

& $serverExecutable
