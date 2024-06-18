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
pip install -r CompleteNotification/requirements.txt

Write-Output "Updating Path environment variable"

$predefinedAliasScriptsFolderPath = "predefinedAliasScripts"
$userAliasScriptsFolderPath = "userAliasScripts"

$parentDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

$predefinedAliasScriptsAbsolutePath = Get-AbsolutePath -ParentFolderPath $parentDirectory -RelativePath $predefinedAliasScriptsFolderPath
$userAliasScriptsAbsolutePath = Get-AbsolutePath -ParentFolderPath $parentDirectory -RelativePath $userAliasScriptsFolderPath

Write-Output "Predefined aliases folder path: $predefinedAliasScriptsAbsolutePath"
Write-Output "User aliases folder path: $userAliasScriptsAbsolutePath"

Write-Output "Updating system path variable..."
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$updatedPath = $currentPath + ";" + $predefinedAliasScriptsAbsolutePath + ";" + $userAliasScriptsAbsolutePath

[System.Environment]::SetEnvironmentVariable("Path", $updatedPath, [System.EnvironmentVariableTarget]::Machine)

Write-Output "Successfully updated!"
