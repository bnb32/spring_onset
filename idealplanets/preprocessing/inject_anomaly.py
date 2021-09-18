import idealplanets.environment as env

import argparse
import Nio
import numpy as np
import os
import sys

parser=argparse.ArgumentParser(description="Inject Anomaly")
parser.add_argument('-aqua',default=False,action='store_true')
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-drycore_topo',default=False,action='store_true')
parser.add_argument('-lapse_rate',default=False,action='store_true')
parser.add_argument('-surface',default=False,action='store_true')
parser.add_argument('-data_dir',default=env.CESM_DATA_DIR)
parser.add_argument('-sst_file',default=env.BASE_SST_FILE)
parser.add_argument('-topo_file',default=env.BASE_TOPO_FILE)
parser.add_argument('-tref_file',default=env.BASE_TREF_FILE)
parser.add_argument('-sst_outfile',default=os.path.splitext(env.BASE_SST_FILE)[0]+"_anomaly.nc")
parser.add_argument('-topo_outfile',default=os.path.splitext(env.BASE_TOPO_FILE)[0]+"_anomaly.nc")
parser.add_argument('-tref_outfile',default=os.path.splitext(env.BASE_TREF_FILE)[0]+"_anomaly.nc")
parser.add_argument('-anomaly_type',default='zonal_band',type=str,choices=['disk','zonal_band','meridional_band','none'])
parser.add_argument('-max_anomaly',type=float,default=5.0)
parser.add_argument('-anomaly_radius',type=float,default=5.0)
parser.add_argument('-anomaly_lat',type=float,default=30.0)
parser.add_argument('-anomaly_lon',type=float,default=0.0)
args=parser.parse_args()

squared_radius = (args.anomaly_radius)**2

if args.aqua:
    basefile=args.data_dir+'/'+args.sst_file
    outfile=args.data_dir+'/'+args.sst_outfile
    f=Nio.open_file(basefile,'r')
    data=f.variables['SST_cpl'].get_value()

elif args.drycore:
    basefile=args.data_dir+'/'+args.tref_file
    outfile=args.data_dir+'/'+args.tref_outfile
    f=Nio.open_file(basefile,'r')
    data=f.variables['tref'].get_value()

elif args.drycore_topo:    
    basefile=args.data_dir+'/'+args.topo_file
    outfile=args.data_dir+'/'+args.topo_outfile
    f=Nio.open_file(basefile,'r')
    data=f.variables['PHIS'].get_value()

    #we assume a temp anomaly coresponds to a change 
    #in phi according to dT/dz = -mg/R (gamma-1)/gamma, 
    #the dry adiabatic lapse rate
    #args.max_anomaly*=-1000.0

    #lets just pass topo anomaly as km
    args.max_anomaly*=9.8*1000.0

else:
    print("Select valid case for anomaly injection")
    exit()

lats=f.variables['lat'].get_value()
lons=f.variables['lon'].get_value()
f.close()

def zonal_band_anomaly_squared_distance(y,y0):
    return (y-y0)**2

def meridional_band_anomaly_squared_distance(r,x,x0,y):
    ymin=np.sqrt(r)+1
    ymax=90-ymin-1
    if ymin<y<ymax: return (x-x0)**2
    elif y<=ymin: return (x-x0)**2+(y-ymin)**2
    elif y>=ymax: return (x-x0)**2+(y-ymax)**2

def disk_anomaly_squared_distance(x,x0,y,y0):
    return (x-x0)**2+(y-y0)**2

def anomaly_smoothing(max_val,d,r):
    if d<=r:
        return max_val*(r-d)/r#*np.exp(-dd/r)
    else:
        return 0

def anomaly_value(max_val,r,x,x0,y,y0):
    if x>=180.0: x-=360.0
    if x0>=180.0: x0-=360.0
    if args.anomaly_type=='disk':
        d=disk_anomaly_squared_distance(x,x0,y,y0)
    if args.anomaly_type=='zonal_band':
        d=zonal_band_anomaly_squared_distance(y,y0)
    if args.anomaly_type=='meridional_band':
        d=meridional_band_anomaly_squared_distance(r,x,x0,y)
    if args.anomaly_type=='none':
        return 0
    return anomaly_smoothing(max_val,np.sqrt(d),np.sqrt(r))

for i,lat in enumerate(lats):
    for j,lon in enumerate(lons):
        
        value=anomaly_value(args.max_anomaly,squared_radius,lon,args.anomaly_lon,lat,args.anomaly_lat)

        if args.aqua:
	        data[:,i,j]+=value
        elif args.drycore:
            if args.lapse_rate:
                for k in range(len(data[0,:,0,0])):
                    lapse_rate=value/(len(data[0,:,0,0])-1)
                    data[:,k,i,j]+=k*lapse_rate
            elif args.surface:
                data[:,-1,i,j]+=value
            else:
                data[:,:,i,j]+=value

os.system('cp %s %s' %(basefile,outfile))
f=Nio.open_file(outfile,'w')
print("**Injecting anomaly: %s**" %(outfile))

if args.aqua:
    f.variables['SST_cpl'].assign_value(data)
if args.drycore:
    f.variables['tref'].assign_value(data)
if args.drycore_topo:
    f.variables['PHIS'].assign_value(data)

#f.variables['time'].units="days since 0001-01-01 00:00:00"
f.close() 
