
"""Plot steadystate"""
import os
import sys

from idealplanets import plot_spectrum_argparse
from idealplanets.environment import EnvironmentConfig


if __name__ == '__main__':
    parser = plot_spectrum_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.outdir is None:
        args.outdir = "%s/figs" % (config.SCRATCH_DIR)

    case_name = (args.infile).split('/')[-1]
    tmp = case_name.split('.cam')
    case_name = tmp[0]
    suffix = 'cam' + tmp[1]
    args.outdir += "/%s/" % (case_name)

    if args.drycore:
        case_type = "drycore"
    elif args.aqua:
        case_type = "aqua"
    else:
        print("Select valid case type\n")
        sys.exit()

    control_file = "%s/cases/archive/%s_control/atm/hist/%s_control.%s" % (
        config.SCRATCH_DIR, case_type, case_type, suffix)

    cmd = 'module load ncl/6.6.2'
    cmd += "; mkdir -p %s" % (args.outdir)
    cmd += '; ncl \'outdir="%s"\' \'cfile="%s"\' \'infile="%s"\' '
    cmd += '\'case_name="%s"\' \'field="%s"\' level=%s ./find_steadystate.ncl'
    cmd = cmd % (args.outdir, control_file, args.infile, case_name, args.field,
                 args.level)
    os.system(cmd)
