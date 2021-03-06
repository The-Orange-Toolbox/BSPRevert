import os
import argparse
import traceback
from datetime import datetime

from valvebsp import Bsp
from valvevmf import Vmf, VmfNode

from brushes import make_world
from entities import make_entities

from totcommon.logger import print_header, stdout
from totcommon.updater import check_updates
from totcommon.reporter import ErrorReporter
from totcommon.stopwatch import StopWatch

from _constants import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Decompile .bsp files into .vmf files to be edited.')

    parser.add_argument('input', metavar='path', type=ascii,
                        help='The path of the BSP to read.')

    parser.add_argument('-o', '--output', metavar='path', type=ascii, default='',
                        help='Where to save the generated vmf (named after original if not specified)')

    parser.add_argument('-v', '--version', action='version', version=VERSION)

    args = parser.parse_args()

    print_header(ORGNAME, NAME, BUILD_DATE)
    check_updates(NAME, VERSION, URL)

    in_bsp = eval(args.input)
    out_vmf = eval(args.output) or in_bsp.replace('.bsp', '.vmf')

    with ErrorReporter(NAME, URL), StopWatch():
        stdout('Loading {}'.format(os.path.abspath(in_bsp)))

        bsp = Bsp(in_bsp)
        vmf = Vmf()

        #vmf.nodes = vmf.nodes + make_entities(bsp)
        vmf.nodes.append(make_world(bsp))

        stdout('Writing {}'.format(os.path.abspath(out_vmf)))
        vmf.save(out_vmf)
