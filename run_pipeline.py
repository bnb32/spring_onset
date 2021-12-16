import argparse
import os,sys
import time
import datetime
import subprocess

import idealplanets.environment

parser=argparse.ArgumentParser(description="Run CESM pipeline")
parser.add_argument('-anomaly_lat',type=float,default=30.0)
parser.add_argument('-anomaly_lon',type=float,default=0.0)
parser.add_argument('-anomaly_radius',type=float,default=10.0)
parser.add_argument('-max_anomaly',type=float,default=5.0)
parser.add_argument('-anomaly_type',default='zonal_band',type=str,choices=['disk','zonal_band','meridional_band','none'])
parser.add_argument('-field',default='PS',type=str)
parser.add_argument('-walltime',default="5:00:00")
parser.add_argument('-out_tstep',default=24)
parser.add_argument('-ndays',default=200,type=int)
parser.add_argument('-start_date',default="1980-03-15")
parser.add_argument('-control',default=False,action='store_true')
parser.add_argument('-norun',default=False,action='store_true')
parser.add_argument('-aqua',default=False,action='store_true')
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-lapse_rate',default=False,action='store_true')
parser.add_argument('-surface',default=False,action='store_true')
parser.add_argument('-drycore_topo',default=False,action='store_true')
parser.add_argument('-ntasks',type=int,default=128)
parser.add_argument('-rebuild',default=False,action='store_true')


args=parser.parse_args()
start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")
stop_date=(start_date + datetime.timedelta(days=args.ndays)).strftime("%Y%m%d")

if args.aqua: 
   if args.control or args.anomaly_type=='none':
       args.case="aqua_control"
   else:    
       args.case="aqua_anomaly"
elif args.drycore: 
   if args.control or args.anomaly_type=='none':
       args.case="drycore_control"
   else:
       if args.lapse_rate:
           args.case="drycore_lapse_anomaly"
       elif args.surface:
           args.case="drycore_surface_anomaly"
       else:
           args.case="drycore_anomaly"

elif args.drycore_topo: 
   if args.control or args.anomaly_type=='none':
       args.case="drycore_topo_control"
   else:
       args.case="drycore_topo_anomaly"
else: 
    print("Select valid case: <aqua/drycore/cam>")
    exit()

aqua_sst_file=env.BASE_SST_FILE
drycore_topo_file=env.BASE_TOPO_FILE
drycore_tref_file=env.BASE_TREF_FILE

if not args.control and not args.anomaly_type=='none':

    args.case=args.case+'_'+args.anomaly_type+'_val%s_rad%s_lat%s_lon%s'%(args.max_anomaly,args.anomaly_radius,int(args.anomaly_lat),int(args.anomaly_lon))

    aqua_sst_file=drycore_tref_file='%s.nc'%(args.case)

    inject_cmd='python %s/inject_anomaly.py -anomaly_type %s -anomaly_radius %s -max_anomaly %s -anomaly_lat %s -anomaly_lon %s'%(env.PRE_PROC_DIR,args.anomaly_type,args.anomaly_radius,args.max_anomaly,args.anomaly_lat,args.anomaly_lon)
    
    if args.aqua: 
        inject_cmd+=' -aqua -sst_outfile %s' %(aqua_sst_file)
    elif args.drycore: 
        inject_cmd+=' -drycore -tref_outfile %s' %(drycore_tref_file)
        if args.lapse_rate:
            inject_cmd+=' -lapse_rate'
    elif args.drycore_topo: 
        inject_cmd+=' -drycore -topo_outfile %s' %(drycore_topo_file)
    
    os.system(inject_cmd)

if not args.norun:

    run_cesm_cmd='python %s/run_cesm.py -walltime %s -start_date %s -stop_date %s -run -case ./cases/%s -ntasks %s -out_tstep %s '%(env.MAIN_DIR,args.walltime,args.start_date,stop_date,args.case,args.ntasks,args.out_tstep)

    
    if args.rebuild:
        run_cesm_cmd+='-rebuild '
	print("**Removing %s/%s**" %(env.CIME_OUTPUT_ROOT,args.case))
	os.system('rm -rf %s/%s' %(env.CIME_OUTPUT_ROOT,args.case))
    elif not os.path.exists("%s/%s" %(env.CIME_OUTPUT_ROOT,args.case)):
        run_cesm_cmd+='-rebuild '
         
    if args.aqua:
        run_cesm_cmd+="-sst_file %s -aqua"%(aqua_sst_file)

    elif args.drycore:
        run_cesm_cmd+="-tref_file %s -drycore"%(drycore_tref_file)

    os.system(run_cesm_cmd)
