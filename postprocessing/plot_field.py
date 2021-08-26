import os,sys
import argparse
sys.path.append('/glade/u/home/bbenton/spring_onset/')
sys.path.append('/glade/u/home/bbenton/spring_onset/postprocessing/')
import environment as env

parser=argparse.ArgumentParser(description="Plot CESM field")
parser.add_argument('-infile',required=True,type=str)
parser.add_argument('-outdir',default="%s/figs"%(env.SCRATCH_DIR),type=str)
parser.add_argument('-field',default="Z3",type=str)
parser.add_argument('-level',default=250,type=int)
parser.add_argument('-substeps',default=1,type=int)
parser.add_argument('-avg',default=False,action='store_true')
parser.add_argument('-gif',default=False,action='store_true')
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-aqua',default=False,action='store_true')
parser.add_argument('-skip_figs',default=False,action='store_true')
parser.add_argument('-anomaly',default=False,action='store_true')
parser.add_argument('-control',default=False,action='store_true')
parser.add_argument('-spectrum',default=False,action='store_true')


args=parser.parse_args()

case_name=(args.infile).split('/')[-1]
tmp=case_name.split('.cam')
case_name=tmp[0]
suffix='cam'+tmp[1]

if args.drycore: 
    case_type="drycore"
elif args.aqua: 
    case_type="aqua"
else:
    print("Select valid case type\n")
    exit()

if args.control:
    case_name=case_type+"_control"

if args.anomaly and not args.control:
    args.outdir+="/%s_anomaly/" %(case_name)
else:
    args.outdir+="/%s/" %(case_name)

base_sst_file="%s/%s"%(env.CESM_DATA_DIR,env.BASE_SST_FILE)
base_tref_file="%s/%s"%(env.CESM_DATA_DIR,env.BASE_TREF_FILE)
anomaly_file="%s/%s.nc"%(env.CESM_DATA_DIR,case_name)
control_file="%s/cases/archive/%s_control/atm/hist/%s_control.%s"%(env.SCRATCH_DIR,case_type,case_type,suffix)

cmd='module load ncl/6.6.2'
cmd+="; mkdir -p %s" %(args.outdir)

if not args.avg:
    cmd+="; rm -rf %s/%s_%s_%s_*.png" %(args.outdir,args.field,args.level,case_name)

if not args.skip_figs:
    cmd+='; ncl \'outdir="%s"\' \'AVG="%s"\' \'ANOMALY="%s"\' \'CONTROL="%s"\' \'cfile="%s"\' \'infile="%s"\' \'case_name="%s"\' \'case_type="%s"\' \'field="%s"\' level=%s substeps=%s \'anomaly_file="%s"\' \'base_sst_file="%s"\' \'base_tref_file="%s"\'   %s/plot_field.ncl' %(args.outdir,args.avg,args.anomaly,args.control,control_file,args.infile,case_name,case_type,args.field,args.level,args.substeps,anomaly_file,base_sst_file,base_tref_file,env.POST_PROC_DIR)

if args.gif and not args.avg:
    cmd+='; convert -delay 20 -loop 0 %s/%s_%s_%s_*.png %s/%s_%s_%s.gif'%(args.outdir,args.field,args.level,case_name,args.outdir,args.field,args.level,case_name)

if args.spectrum:
    cmd+='; ncl \'ANOMALY="%s"\' \'CONTROL="%s"\' \'outdir="%s"\' \'cfile="%s"\' \'infile="%s"\' \'case_name="%s"\' \'field="%s"\' level=%s %s/plot_spectrum.ncl' %(args.anomaly,args.control,args.outdir,control_file,args.infile,case_name,args.field,args.level,env.POST_PROC_DIR)

os.system(cmd)    
