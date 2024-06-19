import os
import sys
import threading
import argparse
from playsound import playsound
from plyer import notification

# Set to False if you don't want to play the sound by default
IS_SOUND_ENABLED = True
script_dir = os.path.dirname(os.path.abspath(__file__))

def _play_sound():
    if IS_SOUND_ENABLED:
        playsound(os.path.join(script_dir, r'assets\success.mp3'))

def handle_done_notification(op_name, no_sound):
    message = 'Unnamed operation' if op_name == None or op_name.isspace() else op_name

    if no_sound == 0:
        sound_thread = threading.Thread(target=_play_sound)
        sound_thread.start()

    notification.notify(
        title='Operation finished!',
        message=message,
        app_name='Scripts',
        timeout=0,
    )

