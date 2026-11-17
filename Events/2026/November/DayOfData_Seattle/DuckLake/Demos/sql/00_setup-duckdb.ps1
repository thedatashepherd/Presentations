# Run in: PowerShell terminal.

# Install DuckDB 2.0.0 locally and download the DuckLake and PostgreSQL
# extensions.
# Run once in PowerShell on Windows with an internet connection.
# The files go under .tools/ in this project; the exports/ folder is
# also created.

$ErrorActionPreference = 'Stop'
$demoRoot = Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Path (Join-Path $demoRoot 'exports') -Force | Out-Null
# Use the same engine version throughout these examples.
$version = '2.0.0'
$installFolder = Join-Path $demoRoot ".tools/duckdb-$version"
$executable = Join-Path $installFolder 'duckdb.exe'
# Download the CLI from the official DuckDB GitHub release if it is
# missing.
if (-not (Test-Path -LiteralPath $executable)) {
    New-Item -ItemType Directory -Path $installFolder -Force | Out-Null
    $archivePath = Join-Path $installFolder 'duckdb-cli-windows-amd64.tar.gz'
    Invoke-WebRequest -Uri "https://github.com/duckdb/duckdb/releases/download/v$version/duckdb-cli-windows-amd64.tar.gz" -OutFile $archivePath
    & tar -xzf $archivePath -C $installFolder
    if ($LASTEXITCODE -ne 0) { throw 'DuckDB archive extraction failed.' }
}
# Verify the CLI version before installing extensions.
$versionOutput = & $executable --version
if ($LASTEXITCODE -ne 0 -or $versionOutput -notmatch '^v2\.0\.0\b') {
    throw 'The installed CLI does not report the expected DuckDB v2.0.0 version.'
}
Write-Host $versionOutput
# Cache both extensions so later connections can load them locally.
& $executable -c 'INSTALL ducklake; INSTALL postgres;'
if ($LASTEXITCODE -ne 0) { throw 'Extension installation failed.' }
Write-Host 'DuckDB 2.0.0 and the DuckLake and PostgreSQL extensions are installed.'

# Result: DuckDB 2.0.0 and both extensions are installed locally.
# PostgreSQL and the lakehouse have not been started.
