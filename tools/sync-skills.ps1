param(
    [string]$Skill = "m-docs",
    [string]$InstallRoot = "$env:USERPROFILE/.codex/skills"
)

$ErrorActionPreference = "Stop"

function Copy-CleanTree {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (Test-Path $Destination) {
        Remove-Item -Recurse -Force $Destination
    }

    $parent = Split-Path -Parent $Destination
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    Copy-Item -Recurse -Force $Source $Destination
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sourceDir = Join-Path $repoRoot "skills/$Skill"
$distDir = Join-Path $repoRoot "dist/codex/$Skill"
$installDir = Join-Path $InstallRoot $Skill
$manifestPath = Join-Path $repoRoot "manifests/$Skill.json"

if (-not (Test-Path $sourceDir)) {
    throw "Skill source not found: $sourceDir"
}

Copy-CleanTree -Source $sourceDir -Destination $distDir

$buildInfo = [ordered]@{
    name = $Skill
    built_at = (Get-Date).ToString("o")
    source_dir = "skills/$Skill"
    install_mode = "copy"
}

if (Test-Path $manifestPath) {
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.version) {
        $buildInfo.version = $manifest.version
    }
}

$buildInfoPath = Join-Path $distDir ".build-info.json"
$buildInfo | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $buildInfoPath

if (-not (Test-Path $InstallRoot)) {
    New-Item -ItemType Directory -Path $InstallRoot | Out-Null
}

Copy-CleanTree -Source $distDir -Destination $installDir

Write-Output "source=$sourceDir"
Write-Output "dist=$distDir"
Write-Output "install=$installDir"
