import os
import argparse
import environment as env

os.environ["PATH"]+=":%s"%env.CESM_SCRIPTS

parser=argparse.ArgumentParser(description="Run CESM")
parser.add_argument('-case',default='./cases/aqua',type=str)
parser.add_argument('-aqua',default=False,action='store_true')
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-drycore_topo',default=False,action='store_true')
parser.add_argument('-queue',default='regular')
parser.add_argument('-cam',default=False,action='store_true')
parser.add_argument('-stop_opt',default="none")
parser.add_argument('-stop_n',default="-999")
parser.add_argument('-project',default=env.PROJECT_CODE)
parser.add_argument('-run',default=False,action='store_true')
parser.add_argument('-ntasks',default=128)
parser.add_argument('-out_tstep',default=24)
parser.add_argument('-walltime',default="5:00:00")
parser.add_argument('-start_date',default="1980-03-15")
parser.add_argument('-stop_date',default="19800414")
parser.add_argument('-data_dir',default=env.CESM_DATA_DIR)
parser.add_argument('-sst_file',default=env.BASE_SST_FILE)
parser.add_argument('-topo_file',default=env.BASE_TOPO_FILE)
parser.add_argument('-tref_file',default=env.BASE_TREF_FILE)
parser.add_argument('-cime_out_dir',default=env.CIME_OUTPUT_ROOT)
parser.add_argument('-docn_stream_file',default="user_docn.streams.txt.aquapfile")
parser.add_argument('-docn_mode',default="sst_aquapfile")
parser.add_argument('-rebuild',default=False,action='store_true')
args=parser.parse_args()

cwd=os.getcwd()

if args.aqua:
    args.compset=env.AQUA_COMPSET
    args.res=env.AQUA_RES

elif args.drycore:    
    args.compset=env.DRYCORE_COMPSET
    args.res=env.DRYCORE_RES

else:
    print("Select valid case: <aqua/drycore/cam>")
    exit()

#create_case_cmd='create_newcase --mpilib openmpi --run-unsupported --case %s --res %s --compset %s --project %s --handle-preexisting-dirs r --output-root %s'%(args.case,args.res,args.compset,args.project,args.cime_out_dir)
create_case_cmd='create_newcase --run-unsupported --case %s --res %s --compset %s --project %s --handle-preexisting-dirs r --output-root %s'%(args.case,args.res,args.compset,args.project,args.cime_out_dir)

#changes to xml files
#change_xml_cmd='./xmlchange --subgroup case.run JOB_QUEUE=%s'%(args.queue)
change_xml_cmd='./xmlchange JOB_QUEUE=%s'%(args.queue)
change_xml_cmd+=';./xmlchange --subgroup case.run JOB_WALLCLOCK_TIME=%s'%(args.walltime)
change_xml_cmd+='; ./xmlchange PROJECT=%s'%(args.project)
change_xml_cmd+='; ./xmlchange STOP_OPTION=%s'%(args.stop_opt)
change_xml_cmd+='; ./xmlchange STOP_N=%s'%(args.stop_n)
change_xml_cmd+='; ./xmlchange NTASKS=%s'%(args.ntasks)
change_xml_cmd+='; ./xmlchange RUN_STARTDATE=%s'%(args.start_date)
change_xml_cmd+='; ./xmlchange STOP_DATE=%s'%(args.stop_date)

if args.aqua:
    change_xml_cmd+='; ./xmlchange DOCN_MODE="%s"'%(args.docn_mode)
    change_xml_cmd+='; ./xmlchange DOCN_AQP_FILENAME="%s/%s"'%(args.data_dir,args.sst_file)

def edit_namelists():
    
    os.chdir(cwd)
    nl_cam_file="%s/user_nl_cam"%(args.case)
    nl_cpl_file="%s/user_nl_cpl"%(args.case)
    
    contents=[]
    contents.append('nhtfrq=-%s\n'%(args.out_tstep))
    contents.append('mfilt=365\n')
    
    if args.drycore:
        #pass 
        os.system('cp %s/cesm_mods/*.F90 %s/SourceMods/src.cam/' %(env.MAIN_DIR,args.case))
        
        #contents.append('fincl1 = "TREF"')
        contents.append('&trefread_nl\n')
        contents.append('treffromfile=.True.\n')
        contents.append('treffile="%s/%s"\n' %(args.data_dir,args.tref_file))
    
    if args.drycore_topo:    
        
        contents.append('state_debug_checks=.true.\n')
        contents.append('use_topo_file=.true.\n')
        contents.append('bnd_topo="%s/%s"\n' %(args.data_dir,args.topo_file))
        contents.append('fv_nspltvrm=4\n')
        contents.append('fv_nspltrac=8\n')
        contents.append('fv_nsplit=8\n')

    print("**Changing namelist file: %s**"%(nl_cpl_file))
    with open(nl_cpl_file,'w') as f:
	    f.write('orb_mode="fixed_year"\n')
	    f.write('orb_iyear=%s\n'%((args.start_date).split('-')[0]))
	    f.write('orb_iyear_align=%s\n'%((args.start_date).split('-')[0]))
	    f.close()    


    print("**Changing namelist file: %s**"%(nl_cam_file))
    with open(nl_cam_file,'w') as f:
        for l in contents: f.write(l)
    f.close()
    
    if args.aqua:
        with open('%s/templates/%s'%(env.MAIN_DIR,args.docn_stream_file),'r') as f:
            docn_file=f.read()
    
        os.system('cp %s/templates/%s %s/'%(env.MAIN_DIR,args.docn_stream_file,args.case))
        with open(args.case+'/'+args.docn_stream_file,'w') as f:
            f.write(docn_file.replace('%SST_FILE%',args.sst_file).replace('%SST_DIR%',args.data_dir))
            f.close()

if args.rebuild or not os.path.exists(args.case):
    print("**Removing %s**"%(args.case))
    os.system('rm -rf %s'%(args.case))
    print("**Creating case %s**"%(args.case))
    os.system(create_case_cmd)
    os.chdir(cwd)
    os.system('cp %s/cesm_mods/env_mach_specific.xml %s/' %(env.MAIN_DIR,args.case))
    os.chdir(args.case)
    print("**Changing xml files**")
    os.system(change_xml_cmd)
    print("**Setting up case %s**"%(args.case))
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
    except:
	print("Error submitting case")
	exit()

