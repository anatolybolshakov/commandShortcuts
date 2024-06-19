import argparse
import os
from models.alias_metadata import (
    AliasMetadata,
    read_alias_metadata,
    get_param_type_from_str,
    find_alias_metadata,
    save_alias_files,
    generate_command_alias_file_name
)

# Null parameter value for strings
NULL_PARAM_SYMBOL = '*'

def read_param(param_str):
    if param_str == NULL_PARAM_SYMBOL:
        return None
    else:
        return param_str

parser = argparse.ArgumentParser(description="Shortcut tool")

subparsers = parser.add_subparsers(dest='alias')
subparsers.required = True

# Common paths
root_dir = os.path.dirname(__file__)
command_files_path = os.path.join(root_dir, 'data', 'command_files')
alias_metadata_file_path = os.path.join(root_dir, 'data', 'alias_metadata.json')

alias_collection = read_alias_metadata(alias_metadata_file_path)

for alias_metadata in alias_collection.aliasesMetadata:
    for alias in alias_metadata.aliases:
        alias_parser = subparsers.add_parser(alias, description=alias_metadata.description)
        for param in alias_metadata.params:
            type_value = get_param_type_from_str(param.type)
            nargs = None if param.default is None else '?'
            alias_parser.add_argument(param.name, type=type_value, help=param.description, nargs=nargs, default = param.default)

args = parser.parse_args()

alias_metadata = find_alias_metadata(args.alias, alias_collection)

if alias_metadata is None:
    raise Exception(f'Not found metadata for alias {args.alias}. Make sure this alias is registered')

if alias_metadata.type == 'finish_notification':
    from complete_notification.done_notification import handle_done_notification
    handle_done_notification(read_param(args.op_name), read_param(args.no_sound))

if alias_metadata.type == 'retry':
    print('Retry command!')

if alias_metadata.type == 'custom':
    from custom_command.custom_command_handler import handle_custom_command
    handle_custom_command(alias_metadata.command, alias_metadata.command_file, command_files_path)

if alias_metadata.type == 'register_alias':
    aliases_list = read_param(args.aliases).split(' ')
    command_file_path = read_param(args.command_file)
    metadata_file_path = read_param(args.metadata_file)
    if command_file_path is not None:
        command_alias_file_name = generate_command_alias_file_name(aliases_list)

    alias_metadata = AliasMetadata(
        aliases=aliases_list, 
        type_value='custom',
        description=read_param(args.description),
        params=None,
        command=read_param(args.command),
        command_file=command_alias_file_name,
        metadata_file=metadata_file_path
    )
    alias_collection.add_alias_metadata(alias_metadata)

    save_alias_files(command_file_path, metadata_file_path, command_alias_file_name, alias_metadata, command_files_path)
    alias_collection.save_to_file(alias_metadata_file_path)

    print (f"Aliases {', '.join(aliases_list)} successfully added!")

if alias_metadata.type == 'remove_alias':
    aliases_list = read_param(args.aliases).split(' ')
    
    removed_aliases = alias_collection.remove_aliases_metadata(aliases_list, command_files_path)

    alias_collection.save_to_file(alias_metadata_file_path)

    if len(removed_aliases) == 0:
        print('No aliases found to remove')
    else:
        print (f"Aliases {', '.join(removed_aliases)} successfully removed!")

