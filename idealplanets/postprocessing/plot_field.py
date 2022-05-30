"""Plot field"""
import os
import sys

from idealplanets.environment import EnvironmentConfig
from idealplanets import plot_field_argparse


if __name__ == '__main__':
    parser = plot_field_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.outdir is None:
        args.outdir = "%s/figs" % (config.SCRATCH_DIR)

    case_name = (args.infile).split('/')[-1]
    tmp = case_name.split('.cam')
    case_name = tmp[0]
    suffix = 'cam' + tmp[1]

    if "drycore" in case_name:
        args.drycore = True
    if "aqua" in case_name:
        args.aqua = True

    if args.drycore:
        case_type = "drycore"
    elif args.aqua:
        case_type = "aqua"
    else:
        print("Select valid case type\n")
        sys.exit()

    if args.control:
        case_name = case_type + "_control"

    args.outdir += "/%s/" % (case_name)

    base_sst_file = "%s/%s" % (config.CESM_DATA_DIR, config.BASE_SST_FILE)
    base_tref_file = "%s/%s" % (config.CESM_DATA_DIR, config.BASE_TREF_FILE)
    anomaly_file = "%s/%s.nc" % (config.CESM_DATA_DIR, case_name)
    control_file = "%s/cases/archive/%s_control/atm/hist/%s_control.%s"
    control_file = control_file % (config.SCRATCH_DIR, case_type, case_type,
                                   suffix)

    cmd = 'module load ncl/6.6.2'
    cmd += "; mkdir -p %s" % (args.outdir)

    if not args.avg:
        cmd += "; rm -rf %s/%s_%s_%s_*.png" % (args.outdir, args.field,
                                               args.level, case_name)

    if not args.skip_figs:
        cmd += '; ncl \'outdir="%s"\' \'AVG="%s"\' \'ANOMALY="%s"\' '
        cmd += '\'CONTROL="%s"\' \'cfile="%s"\' \'infile="%s"\' '
        cmd += '\'case_name="%s"\' \'case_type="%s"\' \'field="%s"\' '
        cmd += 'level=%s substeps=%s \'anomaly_file="%s"\' '
        cmd += '\'base_sst_file="%s"\' \'base_tref_file="%s"\'   '
        cmd += '%s/plot_field.ncl'
        cmd = cmd % (args.outdir, args.avg, args.anomaly, args.control,
                     control_file, args.infile, case_name, case_type,
                     args.field, args.level, args.substeps, anomaly_file,
                     base_sst_file, base_tref_file, config.POST_PROC_DIR)

    if args.gif and not args.avg:
        cmd += '; convert -delay 20 -loop 0 %s/%s_%s_%s_*.png %s/%s_%s_%s.gif'
        cmd = cmd % (args.outdir, args.field, args.level, case_name,
                     args.outdir, args.field, args.level, case_name)

    if args.spectrum:
        cmd += '; ncl \'ANOMALY="%s"\' \'CONTROL="%s"\' \'outdir="%s"\' '
        cmd += '\'cfile="%s"\' \'infile="%s"\' \'case_name="%s"\' '
        cmd += '\'field="%s"\' level=%s %s/plot_spectrum.ncl'
        cmd = cmd % (args.anomaly, args.control, args.outdir, control_file,
                     args.infile, case_name, args.field, args.level,
                     config.POST_PROC_DIR)

    os.system(cmd)
