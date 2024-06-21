import time
from .custom_command_handler import execute_command_text

def execute_with_retries(command, retries_count, delay_between_retries):
    remaining_retries_count = retries_count
    while remaining_retries_count >= 0:
        try:
            execute_command_text(command)
            break
        except Exception as e:
            print(f'Failed to execute command. Error: {e}')
            if remaining_retries_count > 0:
                print(f'Retrying ({remaining_retries_count} of {retries_count}) in {delay_between_retries} ms...')
                time.sleep(delay_between_retries / 1000) 
                remaining_retries_count = remaining_retries_count - 1
            else:
                raise

    if remaining_retries_count < 0:
        print(f'All {retries_count} retry attempts failed')
