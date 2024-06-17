import os
import sys
import threading
import argparse
from playsound import playsound
from plyer import notification

# Set to False if you don't want to play the sound by default
IS_SOUND_ENABLED = True

def play_sound():
    if IS_SOUND_ENABLED:
        playsound(os.path.join(script_dir, 'assets/success.mp3'))


parser = argparse.ArgumentParser(description='Read from console parameters')

parser.add_argument('op_name', type=str, help='Operation Name')
parser.add_argument('no_sound', type=str, help='Set to 1 or o - to turn the sound on/off for notification', default='0')

args = parser.parse_args()


script_dir = os.path.dirname(os.path.abspath(__file__))

message = 'Unnamed operation' if args.op_name.isspace() else args.op_name

if args.no_sound == '0':
    
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.start()

notification.notify(
    title='Operation finished!',
    message=message,
    app_name='Scripts',
    timeout=0,
)
