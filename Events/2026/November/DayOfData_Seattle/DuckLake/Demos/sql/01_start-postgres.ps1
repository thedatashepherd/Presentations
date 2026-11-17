# Run in: PowerShell terminal.

# Start, stop, or check PostgreSQL 17 in Docker. The catalog volume
# survives a stop or restart. Start also launches Docker Desktop.
# Create .env from .env.example before the first start.
#
# Start:   ./sql/01_start-postgres.ps1
# Stop:    ./sql/01_start-postgres.ps1 -Action Stop
# Restart: ./sql/01_start-postgres.ps1 -Action Restart
# Status:  ./sql/01_start-postgres.ps1 -Action Status

[CmdletBinding()]
param(
    [ValidateSet('Start', 'Stop', 'Restart', 'Status')]
    [string]$Action = 'Start'
)

$ErrorActionPreference = 'Stop'
$demoRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker was not found. Install and start Docker Desktop.'
}
function Test-DockerReady {
    # Capture startup errors without interrupting the readiness check.
    try {
        $engine = & docker info --format '{{.OSType}}' 2>$null
        return ($LASTEXITCODE -eq 0 -and $engine -eq 'linux')
    } catch { return $false }
}

if (-not (Test-DockerReady)) {
    if ($Action -notin @('Start', 'Restart')) {
        throw 'Docker Linux engine is not running. Run with -Action Start.'
    }
    $desktop = Join-Path $env:ProgramFiles 'Docker/Docker/Docker Desktop.exe'
    if (-not (Test-Path -LiteralPath $desktop)) {
        throw 'Docker Desktop was not found in Program Files.'
    }
    if (-not (Get-Process 'Docker Desktop' -ErrorAction SilentlyContinue)) {
        Start-Process -FilePath $desktop -WindowStyle Hidden
    }
    Write-Host 'Waiting for Docker Desktop and its Linux engine...'
    $deadline = (Get-Date).AddSeconds(120)
    while (-not (Test-DockerReady)) {
        if ((Get-Date) -ge $deadline) {
            throw 'Docker is not ready. Check Docker Desktop and Linux mode.'
        }
        Start-Sleep -Seconds 2
    }
}

# Resolve Compose and .env from this script without changing folders.
Push-Location -LiteralPath $demoRoot
try {
    switch ($Action) {
        'Start' {
            # Compose downloads the official postgres:17 image if needed.
            & docker compose up -d --wait postgres
        }
        'Stop' {
            # Stop the container; keep the database and Docker Desktop.
            & docker compose stop postgres
        }
        'Restart' {
            & docker compose stop postgres
            if ($LASTEXITCODE -ne 0) { throw 'PostgreSQL stop failed.' }
            & docker compose up -d --wait postgres
        }
        'Status' {
            & docker compose ps -a postgres
        }
    }
    if ($LASTEXITCODE -ne 0) { throw "PostgreSQL $Action failed." }
    if ($Action -ne 'Status') {
        & docker compose ps -a postgres
        if ($LASTEXITCODE -ne 0) { throw 'Status check failed.' }
    }
} finally {
    Pop-Location
}

# Result: Start/Restart waits for readiness on localhost:55432.
# Stop preserves the catalog. Status reports the container state.
