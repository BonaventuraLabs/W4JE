$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $PythonPath)) {
    Write-Error "Python virtual environment not found at '$PythonPath'. Run the Windows quick-start setup first."
    exit 1
}

Push-Location $RepoRoot
try {
    & $PythonPath -m unittest discover -s tests -p "test_*.py" -v
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
