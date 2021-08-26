import Nio,os
import environment as env
import argparse
import numpy as np

parser=argparse.ArgumentParser(description="Initialize base file")
parser.add_argument('-aqua',default=False,action='store_true')
parser.add_argument('-drycore',default=False,action='store_true')
parser.add_argument('-drycore_topo',default=False,action='store_true')
args=parser.parse_args()

if args.aqua:
    f=Nio.open_file(env.ORIG_SST_FILE,'r')
    data=f.variables['SST_cpl'].get_value()
    f.close()
    
    os.system('cp %s %s/%s'%(env.ORIG_SST_FILE,env.CESM_DATA_DIR,env.BASE_SST_FILE))
    f=Nio.open_file(env.CESM_DATA_DIR+'/'+env.BASE_SST_FILE,'w')
    f.variables['SST_cpl'].assign_value(data)
    f.close()

elif args.drycore_topo:
    f=Nio.open_file(env.ORIG_TOPO_FILE,'r')
    data=f.variables['PHIS'].get_value()
    lat=f.variables['lat'].get_value()
    lon=f.variables['lon'].get_value()
    f.close()
    
    os.system('cp %s %s/%s'%(env.ORIG_TOPO_FILE,env.CESM_DATA_DIR,env.BASE_TOPO_FILE))
    os.system('chmod 644 %s/%s' %(env.CESM_DATA_DIR,env.BASE_TOPO_FILE))
    avg_phi=np.mean(data)
    
    for i in range(0,len(lat)):
        for j in range(0,len(lon)):
            data[i,j]=float(0.0)#avg_phi
    
    f=Nio.open_file(env.CESM_DATA_DIR+'/'+env.BASE_TOPO_FILE,'w')
    f.variables['PHIS'].assign_value(data)
    f.close()

elif args.drycore:
    f=Nio.open_file(env.ORIG_TREF_FILE,'r')
    data=f.variables['tref'].get_value()
    lat=f.variables['lat'].get_value()
    lon=f.variables['lon'].get_value()
    lev=f.variables['lev'].get_value()
    f.close()
    
    os.system('cp %s %s/%s'%(env.ORIG_TREF_FILE,env.CESM_DATA_DIR,env.BASE_TREF_FILE))
    os.system('chmod 644 %s/%s' %(env.CESM_DATA_DIR,env.BASE_TREF_FILE))
    avg_tref=np.mean(data)
    
    '''
    for i in range(0,len(lat)):
        for j in range(0,len(lon)):
            for k in range(0,len(lev)):
                data[:,k,i,j]=float(0.0)#avg_phi
    '''

    f=Nio.open_file(env.CESM_DATA_DIR+'/'+env.BASE_TREF_FILE,'w')
    f.variables['tref'].assign_value(data)
    f.close()

else:
    print("Select valid case type")
    exit()
