"""Run cesm"""
import os
import sys

from idealplanets import cesm_argparse
from idealplanets.environment import EnvironmentConfig


def edit_namelists(config, args):
    """Edit namelists before running simulation"""
    os.chdir(cwd)
    nl_cam_file = "%s/user_nl_cam" % (args.case)
    nl_cpl_file = "%s/user_nl_cpl" % (args.case)

    contents = []
    contents.append('nhtfrq=-%s\n' % (args.out_tstep))
    contents.append('mfilt=365\n')

    if args.drycore:
        os.system('cp %s/cesm_mods/*.F90 %s/SourceMods/src.cam/' % (
            config.MAIN_DIR, args.case))

        contents.append('&trefread_nl\n')
        contents.append('treffromfile=.True.\n')
        contents.append('treffile="%s/%s"\n' % (args.data_dir, args.tref_file))

    if args.drycore_topo:

        contents.append('state_debug_checks=.true.\n')
        contents.append('use_topo_file=.true.\n')
        contents.append('bnd_topo="%s/%s"\n' % (args.data_dir, args.topo_file))
        contents.append('fv_nspltvrm=4\n')
        contents.append('fv_nspltrac=8\n')
        contents.append('fv_nsplit=8\n')

    print("**Changing namelist file: %s**" % (nl_cpl_file))
    with open(nl_cpl_file, 'w') as f:
        f.write('orb_mode="fixed_year"\n')
        f.write('orb_iyear=%s\n' % ((args.start_date).split('-')[0]))
        f.write('orb_iyear_align=%s\n' % ((args.start_date).split('-')[0]))
        f.close()

    print("**Changing namelist file: %s**" % (nl_cam_file))
    with open(nl_cam_file, 'w') as f:
        for line in contents:
            f.write(line)
    f.close()

    if args.aqua:
        with open('%s/templates/%s' % (config.MAIN_DIR,
                                       args.docn_stream_file), 'r') as f:
            docn_file = f.read()

        os.system('cp %s/templates/%s %s/' % (config.MAIN_DIR,
                                              args.docn_stream_file,
                                              args.case))
        with open(args.case + '/' + args.docn_stream_file, 'w') as f:
            f.write(docn_file.replace(
                '%SST_FILE%', args.sst_file).replace(
                    '%SST_DIR%', args.data_dir))
            f.close()


if __name__ == '__main__':
    parser = cesm_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.project is None:
        args.project = config.PROJECT_CODE
    if args.data_dir is None:
        args.data_dir = config.CESM_DATA_DIR
    if args.sst_file is None:
        args.sst_file = config.BASE_SST_FILE
    if args.topo_file is None:
        args.topo_file = config.BASE_TOPO_FILE
    if args.tref_file is None:
        args.tref_file = config.BASE_TREF_FILE
    if args.cime_out_dir is None:
        args.cime_out_dir = config.CIME_OUTPUT_ROOT

    cwd = os.getcwd()

    if args.aqua:
        args.compset = config.AQUA_COMPSET
        args.res = config.AQUA_RES

    elif args.drycore:
        args.compset = config.DRYCORE_COMPSET
        args.res = config.DRYCORE_RES

    else:
        print("Select valid case: <aqua/drycore/cam>")
        sys.exit()

    create_case_cmd = 'create_newcase --run-unsupported --case %s --res %s '
    create_case_cmd += '--compset %s --project %s --handle-preexisting-dirs r '
    create_case_cmd += '--output-root %s'
    create_case_cmd = create_case_cmd % (args.case, args.res, args.compset,
                                         args.project, args.cime_out_dir)

    change_xml_cmd = './xmlchange JOB_QUEUE=%s' % (args.queue)
    change_xml_cmd += ';./xmlchange --subgroup case.run JOB_WALLCLOCK_TIME=%s'
    change_xml_cmd = change_xml_cmd % (args.walltime)
    change_xml_cmd += '; ./xmlchange PROJECT=%s' % (args.project)
    change_xml_cmd += '; ./xmlchange STOP_OPTION=%s' % (args.stop_opt)
    change_xml_cmd += '; ./xmlchange STOP_N=%s' % (args.stop_n)
    change_xml_cmd += '; ./xmlchange NTASKS=%s' % (args.ntasks)
    change_xml_cmd += '; ./xmlchange RUN_STARTDATE=%s' % (args.start_date)
    change_xml_cmd += '; ./xmlchange STOP_DATE=%s' % (args.stop_date)

    if args.aqua:
        change_xml_cmd += '; ./xmlchange DOCN_MODE="%s"' % (args.docn_mode)
        change_xml_cmd += '; ./xmlchange DOCN_AQP_FILENAME="%s/%s"'
        change_xml_cmd = change_xml_cmd % (args.data_dir, args.sst_file)

    edit_namelists(config, args)

    if args.rebuild or not os.path.exists(args.case):
        print("**Removing %s**" % (args.case))
        os.system('rm -rf %s' % (args.case))
        print("**Creating case %s**" % (args.case))
        os.system(create_case_cmd)
        os.chdir(cwd)
        os.system('cp %s/cesm_mods/env_mach_specific.xml %s/' % (
            config.MAIN_DIR, args.case))
        os.chdir(args.case)
        print("**Changing xml files**")
        os.system(change_xml_cmd)
        print("**Setting up case %s**" % (args.case))
        os.system('./case.setup')
        edit_namelists()
        os.chdir(cwd)
        os.chdir(args.case)
        os.system('./case.setup --reset')
        os.system('./case.build --clean')
        os.system('./preview_namelists')
        os.system('./case.build')

    else:
        os.chdir(args.case)
        print("**Changing xml files**")
        os.system(change_xml_cmd)
        edit_namelists()
        os.chdir(cwd)
        os.chdir(args.case)
        os.system('./preview_namelists')

    if args.run:
        try:
            os.system('./case.submit')
        except Exception:
            print("Error submitting case")
            sys.exit()
