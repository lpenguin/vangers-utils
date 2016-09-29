"""
usage: vangers-utils <command> [<args>...]

The most commonly used commands are:
   scb        Decode/encode scb
   bmp        Decode/encode bmp
   xbm        Decode/encode xbm

See 'vangers-utils help <command>' for more information on a specific command.
"""

from docopt import docopt

from vangers_utils.cli import scb, bmp, xbm


def main():
    args = docopt(__doc__,
                  options_first=True)
    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'scb':
        scb.main(docopt(scb.__doc__, argv=argv))
    elif args['<command>'] == 'bmp':
        bmp.main(docopt(bmp.__doc__, argv=argv))
    elif args['<command>'] == 'xbm':
        xbm.main(docopt(xbm.__doc__, argv=argv))
    else:
        exit("%r is not a vangers-utils command. See 'vangers-utils  help'." % args['<command>'])
