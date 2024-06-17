# What it is

This is a set of command line aliases - which can be used in CLI (like cmd, PowerShell, other installed - which use Path environment variable as commands source) to simplify speed up some routine operations.

Current shortcuts available:

- 'f' - shows desktop notification and plays sound (can be managed by the parameter)

Can be used for long-running commands - to signalize the end like below:

`long operation; f`

For several commands:
`command1; command2; command3; f`

It will show desktop notification and play sound once it's done.

You can specify operation name which be displayed in notification:

`long operation; f "My long operation 1"`

You can also disable sound using 1 as last argument - it is 0 by default (you would need to pass op name as positional argument first although):

`long operation; f "" 1`

Or you can disable it constantly - by setting up `IS_SOUND_ENABLED` to `False` in the `CompleteNotification\doneNotification.py`.

You can become ninja with a lot of terminals running your commands in parallel, or go grab a coffee while something is being executed - to pick it up in time 🥷☕

## Prerequisites

- PowerShell
- Python v3

## Installation

Run the PowerShell script from the folder root - with Administrator (required to update Path environment variable):

`./install.ps1`

## Plans

Extend with more developer shortcuts.
