#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import sys
from fxns import error, py_version


def main():
    args1 = [('-m', '--marker'), ('-r', '--report'), ('-p', '--prefix')]
    py_version()

    if len(sys.argv) == 1:
        from fxns import msg
        print(msg())
        del msg
        raise SystemExit

    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        import report2plink
        report2plink
        del report2plink
        raise SystemExit

    elif any(x in sys.argv[1:] for x in list(itertools.chain(*args1))):
        x = set([item for item in args1 for a in sys.argv[1:] if a in item])
        y = set([item for item in args1 for a in sys.argv[1:] if a not in item])
        z = list(x.symmetric_difference(y))
        if z:
            error(f'''Missing required argument: {z}
       try `./report2plink -h` for complete arguments list\n''')

        import report2plink
        report2plink
        del report2plink
        raise SystemExit

    else:
        error(f'''Unknown argument(s)
      try ./report2plink -h''')


if __name__ == "__main__":
    main()
