import idealplanets.environment as env

import os,sys
import argparse

parser=argparse.ArgumentParser(description="Plot CESM Spectrum")
parser.add_argument('-infile',required=True,type=str)
parser.add_argument('-outdir',default="%s/figs"%(env.SCRATCH_DIR),type=str)
parser.add_argument('-field',default="KE",type=str)
parser.add_argument('-level',default=250,type=int)
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-aqua',default=False,action='store_true')

args=parser.parse_args()

case_name=(args.infile).split('/')[-1]
tmp=case_name.split('.cam')
case_name=tmp[0]
suffix='cam'+tmp[1]
args.outdir+="/%s/" %(case_name)

if args.drycore: 
    case_type="drycore"
elif args.aqua: 
    case_type="aqua"
else:
    print("Select valid case type\n")
    exit()

control_file="%s/cases/archive/%s_control/atm/hist/%s_control.%s"%(env.SCRATCH_DIR,case_type,case_type,suffix)

cmd='module load ncl/6.6.2'
cmd+="; mkdir -p %s" %(args.outdir)
cmd+='; ncl \'outdir="%s"\' \'cfile="%s"\' \'infile="%s"\' \'case_name="%s"\' \'field="%s"\' level=%s ./find_steadystate.ncl' %(args.outdir,control_file,args.infile,case_name,args.field,args.level)
os.system(cmd)


