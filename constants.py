from enum import Enum

class CommandType(Enum):
    FINISH_NOTIFICATION = 'finish_notification'
    RETRY = 'retry'
    DELAY = 'delay'
    CUSTOM = 'custom'
    REGISTER_ALIAS = 'register_alias'
    REMOVE_ALIAS = 'remove_alias'
    GUI_ALIAS_EDITOR = 'gui_alias_editor'
