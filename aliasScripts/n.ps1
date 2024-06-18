$scriptDirectory = $PSScriptRoot

$pythonScript = Join-Path -Path $scriptDirectory -ChildPath "..\n.py"

$argumentsStr = $args -join ' '

$command = "python $pythonScript $argumentsStr"

Invoke-Expression $command
