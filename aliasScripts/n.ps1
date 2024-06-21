$scriptDirectory = $PSScriptRoot

$pythonScript = Join-Path -Path $scriptDirectory -ChildPath "..\n.py"

$argumentsStr = $args -join ' '

$command = "python $pythonScript $argumentsStr"

Invoke-Expression $command

if ($LASTEXITCODE -ne 0) {
    throw "Command '$command' failed with exit code $LASTEXITCODE"
}
