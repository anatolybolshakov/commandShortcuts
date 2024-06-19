class Config:
    def __init__(self, is_sound_enabled=True):
        self.is_sound_enabled = is_sound_enabled

def read_config(config_file_path):
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    return Config(is_sound_enabled=data['IS_SOUND_ENABLED'])