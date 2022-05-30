"""Plot spectrum"""
from idealplanets import plot_steadystate_argparse
from idealplanets.environment import EnvironmentConfig
import os
import sys


if __name__ == '__main__':
    parser = plot_steadystate_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.outdir is None:
        args.outdir = "%s/figs" % (config.SCRATCH_DIR)
    case_name = (args.infile).split('/')[-1]
    tmp = case_name.split('.cam')
    case_name = tmp[0]
    suffix = 'cam' + tmp[1]

    if args.drycore:
        case_type = "drycore"
    elif args.aqua:
        case_type = "aqua"
    else:
        print("Select valid case type\n")
        sys.exit()

    if args.control:
        case_name = case_type + "_control"

    if args.anomaly and not args.control:
        args.outdir += "/%s_anomaly/" % (case_name)
    else:
        args.outdir += "/%s/" % (case_name)

    control_file = "%s/cases/archive/%s_control/atm/hist/%s_control.%s" % (
        config.SCRATCH_DIR, case_type, case_type, suffix)

    cmd = 'module load ncl/6.6.2'
    cmd += "; mkdir -p %s" % (args.outdir)
    cmd += '; ncl \'ANOMALY="%s"\' \'CONTROL="%s"\' \'outdir="%s"\' '
    cmd += '\'cfile="%s"\' \'infile="%s"\' \'case_name="%s"\' \'field="%s"\' '
    cmd += 'level=%s ./plot_spectrum.ncl'
    cmd = cmd % (args.anomaly, args.control, args.outdir, control_file,
                 args.infile, case_name, args.field, args.level)
    os.system(cmd)
