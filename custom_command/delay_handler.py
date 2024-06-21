import re
import time
from .custom_command_handler import execute_command_text

def execute_with_delay(command, delay_str):
    match = re.match(r"(\d+)(ms|s|m|h)", delay_str)
    if not match:
        print("Invalid delay format. Please use integer followed by 'ms', 's', 'm', or 'h'.")
        return

    delay_value, unit = match.groups()
    delay_value = int(delay_value)

    if unit == "ms":
        delay_seconds = delay_value / 1000
    elif unit == "s":
        delay_seconds = delay_value
    elif unit == "m":
        delay_seconds = delay_value * 60
    elif unit == "h":
        delay_seconds = delay_value * 3600
    else:
        print("Invalid delay unit. Please use 'ms', 's', 'm', or 'h'.")
        return

    print(f'Executing command in {delay_str}...')
    time.sleep(delay_seconds)
    execute_command_text(command)
