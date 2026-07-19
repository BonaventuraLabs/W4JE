$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

$PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    $Message = @"
The W4JE virtual environment was not found at:
$PythonExe

Create it first with:
  py -3.11 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install -r requirements.txt
"@
    Write-Error $Message
    exit 1
}

& $PythonExe -m src.Main
exit $LASTEXITCODE
