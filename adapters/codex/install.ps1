$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$SourceDir = Join-Path $RepoRoot "skills\workovercv"
$TargetDir = Join-Path $RepoRoot ".agents\skills\workovercv"

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path (Join-Path $SourceDir "*") -Destination $TargetDir -Recurse -Force

Write-Output "Installed WorkOverCV skill to $TargetDir"
