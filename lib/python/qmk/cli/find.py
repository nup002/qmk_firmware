"""Command to search through all keyboards and keymaps for a given search criteria.
"""
from milc import cli
from qmk.search import search_keymap_targets


@cli.argument(
    '-f',
    '--filter',
    arg_only=True,
    action='append',
    default=[],
    help=  # noqa: `format-python` and `pytest` don't agree here.
    "Filter the list of keyboards based on their info.json data. Accepts the formats key=value, function(key), or function(key,value), eg. 'features.rgblight=true'. Valid functions are 'absent', 'contains', 'exists' and 'length'. May be passed multiple times; all filters need to match. Value may include wildcards such as '*' and '?'."  # noqa: `format-python` and `pytest` don't agree here.
)
@cli.argument('-p', '--print', arg_only=True, action='append', default=[], help="For each matched target, print the value of the supplied info.json key. May be passed multiple times.")
@cli.argument('-km', '--keymap', type=str, default='default', help="The keymap name to build. Default is 'default'.")
@cli.argument('-x', '--disable-parallel-parsing', arg_only=True, action='store_true', help="Disables parallel parsing of files, useful for debugging stalls.")
@cli.subcommand('Find builds which match supplied search criteria.')
def find(cli):
    """Search through all keyboards and keymaps for a given search criteria.
    """

    if len(cli.args.filter) == 0 and len(cli.args.print) > 0:
        cli.log.warning('No filters supplied -- keymaps not parsed, unable to print requested values.')

    targets = search_keymap_targets([('all', cli.args.keymap)], cli.args.filter, cli.args.print, parallel=not cli.args.disable_parallel_parsing)
    for keyboard, keymap, print_vals in targets:
        print(f'{keyboard}:{keymap}')

        for key, val in print_vals:
            print(f'    {key}={val}')
