import argparse

def parse_cmd_line(me):
    """Get options, show help."""
    parser = argparse.ArgumentParser(
        prog=me,
        description=__doc__,
        epilog='Evaling means "eval $({me})"'.format(me=me),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'tmp_root',
        nargs='?',
        help='parent folder of the temp folder',
    )
    return parser.parse_args()
