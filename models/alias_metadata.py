import os
import json
import shutil

from constants import CommandType

def _json_skip_none(obj):
    return {k: v for k, v in obj.__dict__.items() if v is not None}

class AliasMetadata:
    def __init__(self, aliases, type_value, description=None, params=None, command=None, command_file=None, param_boundary_placeholder=None):
        self.aliases = aliases
        self.description = description
        self.type = type_value
        self.params = params
        self.command = command
        self.command_file = command_file
        self.param_boundary_placeholder = param_boundary_placeholder 

class AliasCollection:
    def __init__(self, aliasesMetadata):
        self.aliasesMetadata = aliasesMetadata
        self.aliasesDictionary = {}
        for aliasData in aliasesMetadata:
            for alias in aliasData.aliases:
                self.aliasesDictionary[alias] = aliasData

    def add_alias_metadata(self, alias_metadata):
        already_registered_alias = self.get_first_already_registered_alias(alias_metadata.aliases)
        if already_registered_alias != None:
                raise ValueError(f"Alias '{already_registered_alias}' is already registered. Please use another alias or amend existing registered alias.")
        
        self.aliasesMetadata.append(alias_metadata)
        for alias in alias_metadata.aliases:
            self.aliasesDictionary[alias] = alias_metadata;
    
    def remove_aliases_metadata(self, aliases_list, command_files_path):
        removed_aliases = []
        for alias in aliases_list:

            if alias in self.aliasesDictionary:
                del self.aliasesDictionary[alias]
                removed_aliases.append(alias)
            else:
                print(f"Alias '{alias}' was not found. Skipping...")

        for aliasMetadata in self.aliasesMetadata:
            aliasMetadata.aliases = [alias for alias in aliasMetadata.aliases if alias not in aliases_list]
            remove_alias_files(aliasMetadata, command_files_path)

        if len(aliasMetadata.aliases) == 0:
            self.aliasesMetadata.remove(aliasMetadata)

        return removed_aliases

    def save_to_file(self, alias_metadata_file_path):
        with open(alias_metadata_file_path, 'w') as f:
            json.dump(self.aliasesMetadata, f, default=_json_skip_none, indent=4)
    
    def get_custom_commands_data(self):
        custom_aliases_data = []

        if self.aliasesMetadata == None:
            return custom_aliases_data

        for alias_data in self.aliasesMetadata:
            if alias_data.type == CommandType.CUSTOM.value:
                custom_aliases_data.append(alias_data)

        return custom_aliases_data

    def get_first_already_registered_alias(self, aliases_list):
        for alias in aliases_list:
            if alias in self.aliasesDictionary:
                return alias

        return None

class AliasParameter:
    def __init__(self, name, type_value, description, default=None):
        self.name = name
        self.type = type_value
        self.description = description
        self.default = default

def get_param_type_from_str(type_str):
    if type_str == 'str':
        return str
    elif type_str == 'int':
        return int
    elif type_str == 'float':
        return float
    elif type_str == 'bool':
        return bool
    else:
        raise ValueError(f"Invalid type string: {type_str}")

def read_alias_metadata(alias_metadata_file_path):
    with open(alias_metadata_file_path, 'r') as f:
        data = json.load(f)

    aliases = []
    for item in data:
        params = []
        params_json = item.get('params')
        if params_json is not None:
            for param in params_json:
                params.append(AliasParameter(
                    name=param['name'],
                    type_value=param['type'],
                    description=param.get('description'),
                    default=param.get('default')
                ))
        alias = AliasMetadata(
            aliases=item['aliases'], 
            type_value=item['type'],
            description=item.get('description'),
            params=params,
            command=item.get('command'),
            command_file=item.get('command_file'),
            param_boundary_placeholder=item.get('param_boundary_placeholder')
        )
        aliases.append(alias)

    return AliasCollection(aliasesMetadata=aliases)

def find_alias_metadata(alias, aliases_collection):
    return aliases_collection.aliasesDictionary.get(alias)

def generate_command_alias_file_name(aliases):
    return f"{'_'.join(aliases)}.txt"

def get_formatted_aliases_list(aliases):
    return ' '.join(aliases)

# Note - this method modifies alias_metadata. Refactor in future
def save_alias_metadata_for_command_from_file(command_file_path, metadata_file_path, result_command_file_name, alias_metadata, command_files_path):
    if command_file_path is not None and command_file_path != '':
        copied_command_file_path = os.path.join(command_files_path, result_command_file_name)
        shutil.copy(command_file_path, copied_command_file_path)

    if metadata_file_path is not None and metadata_file_path != '':
        with open(metadata_file_path, 'r') as f:
            data = json.load(f)

        params = []
    
        for param in data:
            params.append(AliasParameter(
                name=param['name'],
                type_value=param['type'],
                description=param.get('description'),
                default=param.get('default')
            ))
        
        alias_metadata.params = params

def save_command_to_file(command_files_path, result_command_file_name, command_content):
    if not os.path.exists(command_files_path):
        os.makedirs(command_files_path)

    result_command_file_path = os.path.join(command_files_path, result_command_file_name)
    with open(result_command_file_path, 'w') as result_file:
        result_file.write(command_content)

# Quotes single or double quotes (' or ") - to keep them for saved commands
def quote_command_text(command_text):
    command_text = command_text.replace("'", "`'")
    command_text = command_text.replace('"', '`"')

    return command_text

def remove_alias_files(alias_metadata, command_files_path):
    if alias_metadata is not None and alias_metadata.command_file is not None:
        copied_command_file_path = os.path.join(command_files_path, alias_metadata.command_file)
        if os.path.isfile(copied_command_file_path):
            os.remove(copied_command_file_path)
        else:
            print(f"Error: command metadata file {copied_command_file_path} not found")

