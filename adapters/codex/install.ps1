$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$SourceDir = Join-Path $RepoRoot "adapters\codex\plugin\workovercv"
$UserHome = [Environment]::GetFolderPath("UserProfile")
if (-not $UserHome) {
    $UserHome = $HOME
}
$PluginsRoot = Join-Path $UserHome "plugins"
$TargetDir = Join-Path $PluginsRoot "workovercv"
$MarketplaceDir = Join-Path $UserHome ".agents\plugins"
$MarketplacePath = Join-Path $MarketplaceDir "marketplace.json"

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path (Join-Path $SourceDir "*") -Destination $TargetDir -Recurse -Force

New-Item -ItemType Directory -Force -Path $MarketplaceDir | Out-Null

if (Test-Path -LiteralPath $MarketplacePath) {
    $Marketplace = Get-Content -LiteralPath $MarketplacePath -Raw | ConvertFrom-Json
}
else {
    $Marketplace = [pscustomobject][ordered]@{
        name = "personal"
        interface = [pscustomobject][ordered]@{
            displayName = "Personal"
        }
        plugins = @()
    }
}

if (-not ($Marketplace.PSObject.Properties.Name -contains "plugins")) {
    $Marketplace | Add-Member -MemberType NoteProperty -Name plugins -Value @()
}

$ExistingPlugins = @($Marketplace.plugins | Where-Object { $_.name -ne "workovercv" })
$WorkOverCvEntry = [pscustomobject][ordered]@{
    name = "workovercv"
    source = [pscustomobject][ordered]@{
        source = "local"
        path = "./plugins/workovercv"
    }
    policy = [pscustomobject][ordered]@{
        installation = "AVAILABLE"
        authentication = "ON_INSTALL"
    }
    category = "Productivity"
}

$Marketplace.plugins = @($ExistingPlugins + $WorkOverCvEntry)
$MarketplaceJson = ($Marketplace | ConvertTo-Json -Depth 20) + [Environment]::NewLine
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($MarketplacePath, $MarketplaceJson, $Utf8NoBom)

Write-Output "Installed WorkOverCV plugin source to $TargetDir"
Write-Output "Updated personal marketplace at $MarketplacePath"
Write-Output "Run: codex plugin add workovercv@$($Marketplace.name)"
