import os
import subprocess
import shutil

def handle_custom_command(command, command_file, command_files_path):
    command_text = command
    if command_text is None:
        command_file_path = os.path.join(command_files_path, command_file)
        with open(command_file_path, 'r') as f:
            command_text = f.read().strip()
    
    # Using Powershell 7 by default if exists, otherwise - using Powershell
    powershell_command = 'pwsh.exe' if shutil.which('pwsh.exe') else 'powershell.exe'
    process = subprocess.Popen([powershell_command, '-Command', command_text], cwd='.')
    process.wait()
