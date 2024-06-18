import argparse
from complete_notification.done_notification import handle_done_notification


parser = argparse.ArgumentParser(description="Shortcut tool")

subparsers = parser.add_subparsers(dest='alias')
subparsers.required = True

parser_f = subparsers.add_parser('f', description="Shows desktop notification on finish and plays sound (optional)")

parser_f.add_argument('op_name', type=str, help='Operation Name', nargs='?', default = None)
parser_f.add_argument('no_sound', type=int, help='Set to 1 or 0 - to turn the sound on/off for notification', nargs='?', default=0)

parser_r = subparsers.add_parser('r', description="Retries specified command")

args = parser.parse_args()

if args.alias == 'f':
    handle_done_notification(args.op_name, args.no_sound)

if args.alias == 'r':
    print('Retry command!')
