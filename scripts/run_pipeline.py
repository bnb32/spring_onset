"""Run cesm pipeline with injection"""
import os
import sys
import datetime

from idealplanets import run_cesm_pipeline_argparse
from idealplanets.environment import EnvironmentConfig


if __name__ == '__main__':

    parser = run_cesm_pipeline_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")
    stop_date = (start_date
                 + datetime.timedelta(days=args.ndays)).strftime("%Y%m%d")

    if args.aqua:
        if args.control or args.anomaly_type == 'none':
            args.case = "aqua_control"
        else:
            args.case = "aqua_anomaly"
    elif args.drycore:
        if args.control or args.anomaly_type == 'none':
            args.case = "drycore_control"
        else:
            if args.lapse_rate:
                args.case = "drycore_lapse_anomaly"
            elif args.surface:
                args.case = "drycore_surface_anomaly"
            else:
                args.case = "drycore_anomaly"

    elif args.drycore_topo:
        if args.control or args.anomaly_type == 'none':
            args.case = "drycore_topo_control"
        else:
            args.case = "drycore_topo_anomaly"
    else:
        print("Select valid case: <aqua/drycore/cam>")
        sys.exit()

    aqua_sst_file = config.BASE_SST_FILE
    drycore_topo_file = config.BASE_TOPO_FILE
    drycore_tref_file = config.BASE_TREF_FILE

    if not args.control and not args.anomaly_type == 'none':

        args.case = args.case + '_' + args.anomaly_type
        args.case += '_val%s_rad%s_lat%s_lon%s' % (args.max_anomaly,
                                                   args.anomaly_radius,
                                                   int(args.anomaly_lat),
                                                   int(args.anomaly_lon))

        aqua_sst_file = drycore_tref_file = '%s.nc' % (args.case)

        inject_cmd = 'python %s/inject_anomaly.py -anomaly_type %s '
        inject_cmd += '-anomaly_radius %s -max_anomaly %s -anomaly_lat %s '
        inject_cmd += '-anomaly_lon %s'
        inject_cmd = inject_cmd % (config.PRE_PROC_DIR, args.anomaly_type,
                                   args.anomaly_radius, args.max_anomaly,
                                   args.anomaly_lat, args.anomaly_lon)

        if args.aqua:
            inject_cmd += ' -aqua -sst_outfile %s' % (aqua_sst_file)
        elif args.drycore:
            inject_cmd += ' -drycore -tref_outfile %s' % (drycore_tref_file)
            if args.lapse_rate:
                inject_cmd += ' -lapse_rate'
        elif args.drycore_topo:
            inject_cmd += ' -drycore -topo_outfile %s' % (drycore_topo_file)

        os.system(inject_cmd)

    if not args.norun:
        run_cesm_cmd = 'python %s/run_cesm.py -walltime %s -start_date %s '
        run_cesm_cmd += '-stop_date %s -run -case ./cases/%s -ntasks %s '
        run_cesm_cmd += '-out_tstep %s '
        run_cesm_cmd = run_cesm_cmd % (config.MAIN_DIR, args.walltime,
                                       args.start_date, stop_date,
                                       args.case, args.ntasks,
                                       args.out_tstep)

        if args.rebuild:
            run_cesm_cmd += '-rebuild '
            print("**Removing %s/%s**" % (config.CIME_OUTPUT_ROOT, args.case))
            os.system('rm -rf %s/%s' % (config.CIME_OUTPUT_ROOT, args.case))

        elif not os.path.exists("%s/%s" % (config.CIME_OUTPUT_ROOT,
                                           args.case)):
            run_cesm_cmd += '-rebuild '

        if args.aqua:
            run_cesm_cmd += "-sst_file %s -aqua" % (aqua_sst_file)

        elif args.drycore:
            run_cesm_cmd += "-tref_file %s -drycore" % (drycore_tref_file)

        os.system(run_cesm_cmd)
