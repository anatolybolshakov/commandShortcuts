$scriptDirectory = $PSScriptRoot

$pythonScript = Join-Path -Path $scriptDirectory -ChildPath "..\CompleteNotification\doneNotification.py"

$opName = if ($args[0]) { $args[0] } else { " " }
$noSound = if ($args[1]) { $args[1] } else { 0 }

$command = "python $pythonScript `"$opName`" `"$noSound`""

Invoke-Expression $command
