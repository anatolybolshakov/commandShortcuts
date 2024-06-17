# This script installs the quick commands
# f - runs desktop notification and sound. You can use in combination with other commands - to get notification about commands finish

Write-Output "Installing dependencies"
pip install -r CompleteNotification/requirements.txt

Write-Output "Updating Path environment variable"

$relativeCommandsFolderPath = ".\aliasesScripts"

$scriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

$absoluteCommandsFolderPath = Resolve-Path -Path (Join-Path -Path $scriptDirectory -ChildPath $relativeCommandsFolderPath)

Write-Output "Quick commands folder path: $absolutePath"

Write-Output "Updating system path variable..."
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$updatedPath = $currentPath + ";" + $absoluteCommandsFolderPath

[System.Environment]::SetEnvironmentVariable("Path", $updatedPath, [System.EnvironmentVariableTarget]::Machine)

Write-Output "Successfully updated!"
