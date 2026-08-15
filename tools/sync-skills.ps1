param(
    [string]$Skill = "m-docs",
    [string]$InstallRoot = "$env:USERPROFILE/.codex/skills"
)

$ErrorActionPreference = "Stop"

function Test-ExcludedSyncItem {
    param(
        [Parameter(Mandatory = $true)][System.IO.FileSystemInfo]$Item
    )

    if ($Item.PSIsContainer) {
        return $Item.Name -eq "__pycache__"
    }

    return $Item.Extension.ToLowerInvariant() -in @(".pyc", ".pyo")
}

function Copy-TreeContent {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Destination)) {
        New-Item -ItemType Directory -Path $Destination | Out-Null
    }

    foreach ($item in Get-ChildItem -LiteralPath $Source -Force) {
        if (Test-ExcludedSyncItem -Item $item) {
            continue
        }

        $target = Join-Path $Destination $item.Name
        if ($item.PSIsContainer) {
            Copy-TreeContent -Source $item.FullName -Destination $target
        }
        else {
            Copy-Item -LiteralPath $item.FullName -Destination $target -Force
        }
    }
}

function Copy-CleanTree {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (Test-Path -LiteralPath $Destination) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }

    $parent = Split-Path -Parent $Destination
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    Copy-TreeContent -Source $Source -Destination $Destination
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$sourceDir = Join-Path $repoRoot "skills/$Skill"
$distDir = Join-Path $repoRoot "dist/codex/$Skill"
$installDir = Join-Path $InstallRoot $Skill
$manifestPath = Join-Path $repoRoot "manifests/$Skill.json"

if (-not (Test-Path -LiteralPath $sourceDir)) {
    throw "Skill source not found: $sourceDir"
}

Copy-CleanTree -Source $sourceDir -Destination $distDir

$buildInfo = [ordered]@{
    name = $Skill
    built_at = (Get-Date).ToString("o")
    source_dir = "skills/$Skill"
    install_mode = "copy"
}

if (Test-Path -LiteralPath $manifestPath) {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.version) {
        $buildInfo.version = $manifest.version
    }
}

$buildInfoPath = Join-Path $distDir ".build-info.json"
$buildInfo | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $buildInfoPath -Encoding UTF8

if (-not (Test-Path -LiteralPath $InstallRoot)) {
    New-Item -ItemType Directory -Path $InstallRoot | Out-Null
}

Copy-CleanTree -Source $distDir -Destination $installDir

Write-Output "source=$sourceDir"
Write-Output "dist=$distDir"
Write-Output "install=$installDir"
