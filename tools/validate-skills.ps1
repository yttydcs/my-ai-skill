param(
    [string]$Skill = "docs-governor",
    [string]$PythonExe = "",
    [switch]$SkipQuickValidate
)

$ErrorActionPreference = "Stop"

function Resolve-Python {
    param([string]$ExplicitPath)

    if ($ExplicitPath) {
        if (-not (Test-Path $ExplicitPath)) {
            throw "Python executable not found: $ExplicitPath"
        }
        return $ExplicitPath
    }

    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -and $cmd.Source -notmatch "WindowsApps") {
        return $cmd.Source
    }

    $candidates = @()

    $condaRoot = Join-Path $env:USERPROFILE ".conda\\envs"
    if (Test-Path $condaRoot) {
        $candidates += Get-ChildItem -Path $condaRoot -Filter python.exe -Recurse -Depth 2 -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty FullName
    }

    $localPythonRoot = Join-Path $env:LOCALAPPDATA "Programs\\Python"
    if (Test-Path $localPythonRoot) {
        $candidates += Get-ChildItem -Path $localPythonRoot -Filter python.exe -Recurse -Depth 3 -ErrorAction SilentlyContinue |
            Select-Object -ExpandProperty FullName
    }

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    throw "No usable Python executable found. Pass -PythonExe explicitly."
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillDir = Join-Path $repoRoot "skills/$Skill"
$validator = "C:\Users\HelloWorld\.codex\skills\.system\skill-creator\scripts\quick_validate.py"

if (-not (Test-Path $skillDir)) {
    throw "Skill directory not found: $skillDir"
}

$requiredPaths = @(
    (Join-Path $skillDir "SKILL.md"),
    (Join-Path $skillDir "agents/openai.yaml")
)

foreach ($path in $requiredPaths) {
    if (-not (Test-Path $path)) {
        throw "Missing required path: $path"
    }
}

Write-Output "skill=$skillDir"
Write-Output "required_paths=ok"

if (-not $SkipQuickValidate) {
    $python = Resolve-Python -ExplicitPath $PythonExe
    & $python $validator $skillDir
}
