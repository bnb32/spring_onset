import argparse
import os,sys
import time
import subprocess
sys.path.append('./')
import environment as env

parser=argparse.ArgumentParser(description="Run Multiple Instances of CESM Pipeline")
parser.add_argument('-case',default='aqua_anomaly')
parser.add_argument('-anomaly_lat_min',type=float,default=10.0)
parser.add_argument('-anomaly_lat_max',type=float,default=50.0)
parser.add_argument('-anomaly_lon',type=float,default=180.0)
parser.add_argument('-anomaly_lat_increment',type=float,default=5.0)
parser.add_argument('-max_anomaly',type=float,default=5.0)
parser.add_argument('-anomaly_radius_squared',type=float,default=20.0)
parser.add_argument('-anomaly_type',default='zonal_band',type=str)
parser.add_argument('-sims',default=False,action='store_true')

args=parser.parse_args()

args.anomaly_lat=args.anomaly_lat_min
case=args.case+'_'+args.anomaly_type+'_lat%s_lon%s'

if args.sims:
    while args.anomaly_lat <= args.anomaly_lat_max:

        pipeline_cmd='python ./run_pipeline.py -anomaly_type %s -anomaly_radius_squared %s -max_anomaly %s -anomaly_lat %s -anomaly_lon %s' %(args.anomaly_type,args.anomaly_radius_squared,args.max_anomaly,args.anomaly_lat,args.anomaly_lon)
        os.system(pipeline_cmd)

        args.anomaly_lat+=args.anomaly_lat_increment
