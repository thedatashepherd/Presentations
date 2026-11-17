# Run in: PowerShell terminal, or choose DuckDB A / DuckDB B in the
# VS Code terminal dropdown. Both profiles run this script.

# Open a DuckDB session. On your own machine this step is just: duckdb
# No database file is named, so the session is in-memory and the
# prompt starts with "memory".
# This script adds two things for the demo:
#   1. It runs the DuckDB 2.0.0 CLI installed by 00_setup-duckdb.ps1,
#      not whichever duckdb is on PATH.
#   2. It copies POSTGRES_PASSWORD from .env into PGPASSWORD, so
#      05_attach.sql connects without a password in the SQL.
# DuckDB A and DuckDB B are two independent processes started the
# same way. Start each one once.

[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$DuckDbArgs)
$ErrorActionPreference = 'Stop'
# Locate the project from this script, regardless of the current folder.
$demoRoot = Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Path (Join-Path $demoRoot 'exports') -Force | Out-Null

# Use the executable installed by 00_setup-duckdb.ps1.
$duckDbExecutable = Join-Path $demoRoot '.tools/duckdb-2.0.0/duckdb.exe'
if (-not (Test-Path -LiteralPath $duckDbExecutable)) {
    throw 'Run ./sql/00_setup-duckdb.ps1 to install the pinned DuckDB 2.0 CLI.'
}
# Keep credentials in local configuration instead of SQL source.
$envPath = Join-Path $demoRoot '.env'
if (-not (Test-Path -LiteralPath $envPath)) {
    throw 'Copy .env.example to .env and set POSTGRES_PASSWORD before starting.'
}
$passwordLine = Get-Content -LiteralPath $envPath |
    Where-Object { $_ -match '^POSTGRES_PASSWORD=' } | Select-Object -First 1
if (-not $passwordLine -or $passwordLine -eq 'POSTGRES_PASSWORD=') {
    throw 'Set POSTGRES_PASSWORD in .env.'
}
# Pass PGPASSWORD to DuckDB and restore the previous value when it
# exits.
$previousPgPassword = $env:PGPASSWORD
try {
    $env:PGPASSWORD = $passwordLine.Substring('POSTGRES_PASSWORD='.Length)
    # Resolve relative .read sql/... commands from the project folder.
    Push-Location -LiteralPath $demoRoot
    Write-Host 'Starting DuckDB 2.0.0 with an in-memory database.'
    Write-Host 'PostgreSQL credentials loaded from the local .env file.'
    Write-Host '03_versions.sql checks versions.'
    Write-Host '04_duckdb_files.sql queries files without a lake.'
    # With no database filename, each terminal starts its own in-memory
    # process.
    try { & $duckDbExecutable @DuckDbArgs } finally { Pop-Location }
} finally {
    if ($null -eq $previousPgPassword) {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    } else { $env:PGPASSWORD = $previousPgPassword }
}

# Result: While running, this terminal has its own DuckDB session.
# 05_attach.sql connects it to the shared lakehouse.

