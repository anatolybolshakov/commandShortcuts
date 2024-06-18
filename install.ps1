# This script installs the quick commands
# f - runs desktop notification and sound. You can use in combination with other commands - to get notification about commands finish

function Get-AbsolutePath() {
    param (
        [string]$ParentFolderPath,
        [string]$RelativePath
    )

    return Resolve-Path -Path (Join-Path -Path $ParentFolderPath -ChildPath $RelativePath)
}

$ErrorActionPreference = "Stop"

Write-Output "Installing dependencies"
pip install -r requirements.txt

Write-Output "Updating Path environment variable"

$aliasScriptsFolderPath = "aliasScripts"

$parentDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

$aliasScriptsAbsolutePath = Get-AbsolutePath -ParentFolderPath $parentDirectory -RelativePath $aliasScriptsFolderPath

Write-Output "Aliases folder path: $aliasScriptsAbsolutePath"

Write-Output "Updating system path variable..."
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$updatedPath = $currentPath + ";" + $aliasScriptsAbsolutePath

[System.Environment]::SetEnvironmentVariable("Path", $updatedPath, [System.EnvironmentVariableTarget]::Machine)

Write-Output "Successfully updated!"
