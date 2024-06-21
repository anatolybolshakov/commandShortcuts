import os
import subprocess
import shutil

def insert_params_values(command_text, param_boundary_placeholder, passed_params_dict):
    if param_boundary_placeholder is None or param_boundary_placeholder == "":
        command_text = command_text.format(**passed_params_dict)
    else:
        for key, value in passed_params_dict.items():
            placeholder = f'{param_boundary_placeholder}{key}{param_boundary_placeholder}'
            command_text = command_text.replace(placeholder, str(value))

    return command_text

def handle_custom_command(alias_metadata, passed_params_dict, command_files_path):
    command_text = alias_metadata.command
    if command_text is None:
        command_file_path = os.path.join(command_files_path, alias_metadata.command_file)
        with open(command_file_path, 'r') as f:
            command_text = f.read().strip()
    
    command_text = insert_params_values(command_text, alias_metadata.param_boundary_placeholder, passed_params_dict)

    execute_command_text(command_text)

def execute_command_text(command_text):
    # Using Powershell 7 by default if exists, otherwise - using Powershell
    powershell_command = 'pwsh.exe' if shutil.which('pwsh.exe') else 'powershell.exe'
    # process = subprocess.Popen([powershell_command, '-Command', command_text], cwd='.')
    subprocess.check_call([powershell_command, '-Command', command_text], cwd='.')

