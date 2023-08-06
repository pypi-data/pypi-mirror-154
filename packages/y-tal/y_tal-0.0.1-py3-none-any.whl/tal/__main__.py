import argparse
from ast import Assert

parser = argparse.ArgumentParser(
    description='TAL - Transient Auxiliary Library')
subparsers = parser.add_subparsers(
    help='Command', required=True, dest='command')

# render commands
render_parser = subparsers.add_parser(
    'render', help='Create, edit or execute renders of simulated NLOS scene data captures')
render_parser.add_argument('config_file', nargs='*')
render_parser.add_argument('-t', '--threads',
                           type=int, default=1, required=False,
                           help='Number of threads')
render_parser.add_argument('-n', '--nice',
                           type=int, default=0, required=False,
                           help='Change +/- in nice factor. Positive values = lower priority. Negative values = higher priority (needs sudo)')
render_parser.add_argument('--no-steady',
                           type=bool, metavar='do_steady_renders', action='store_false',
                           help='Disable generation of steady state images')
render_parser.add_argument('--no-hdf5',
                           type=bool, metavar='do_store_hdf5', action='store_false',
                           help='Disable generation of hdf5 output')
render_parser.add_argument('--no-ldr',
                           type=bool, metavar='do_convert_ldr', action='store_false',
                           help='Disable conversion of results to LDR')

args = parser.parse_args()

if args.command == 'render':
    config_file = args.config_file
    assert (len(config_file) == 1 and config_file[0].endswith('.yaml')) or \
        (len(config_file) == 2 and config_file[0].lower() == 'new'), \
        'config_file must be one of "new <new_folder_name> or <config_file.yaml>"'
    if config_file[0].lower() == 'new':
        new_folder_name = config_file[1]
        from tal.render import create_nlos_scene
        create_nlos_scene(new_folder_name)
    else:
        from tal.render import render_nlos_scene
        config_file = config_file[0]
        render_nlos_scene(config_file)
else:
    raise AssertionError('Invalid command? Check argparse')
