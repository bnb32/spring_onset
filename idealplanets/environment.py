import os

USERNAME='bbenton'
PROJECT_CODE='UCOR0044'
MAIN_DIR='/glade/u/home/'+USERNAME+'/spring_onset/'
MY_CESM_DIR=MAIN_DIR+'/my_cesm'
POST_PROC_DIR=MAIN_DIR+'/idealplanets/postprocessing/'
PRE_PROC_DIR=MAIN_DIR+'/idealplanets/preprocessing/'
SCRATCH_DIR='/glade/scratch/'+USERNAME+'/'
CIME_OUTPUT_ROOT=SCRATCH_DIR+'/cases/'
CESM_DATA_DIR=SCRATCH_DIR+'/cesm_data/'
CESM_SCRIPTS=MY_CESM_DIR+'/cime/scripts/'
CESM_CAM_OUT_DIR=SCRATCH_DIR+'/archive/%s/atm/hist/'
ORIG_DATA_DIR='/glade/p/cesmdata/cseg/inputdata/'
ORIG_TOPO_DIR=ORIG_DATA_DIR+'/atm/cam/topo/'
ORIG_TREF_DIR=MAIN_DIR+'/trefread/NCL/output/'
ORIG_SST_DIR=ORIG_DATA_DIR+'/ocn/docn7/AQUAPLANET/'
#ORIG_SST_DIR="%s/atm/cam/sst/"%(ORIG_DATA_DIR)
#ORIG_TOPO_FILE="%s/USGS-gtopo30_0.9x1.25_remap_c051027.nc"%(ORIG_TOPO_DIR)
ORIG_TOPO_FILE=ORIG_TOPO_DIR+'/USGS-gtopo30_64x128_c050520.nc'
ORIG_TREF_FILE=ORIG_TREF_DIR+'/tref_T85L30.nc'
ORIG_SST_FILE=ORIG_SST_DIR+'/sst_c4aquasom_0.9x1.25_clim.c170512.nc'
#ORIG_SST_FILE="%s/sst_HadOIBl_bc_64x128_clim_c110526.nc"%(ORIG_SST_DIR)
BASE_SST_FILE='aqua_sst.nc'
BASE_TOPO_FILE='drycore_topo.nc'
BASE_TREF_FILE='drycore_tref.nc'
#AQUA_RES="T42_T42_mg17" 
AQUA_RES="f09_f09_mg17"
AQUA_COMPSET="QPC6"
#DRYCORE_RES="T42z30_T42_mg17"
DRYCORE_RES="T85z30_T85_mg17"
#DRYCORE_RES="f09z30_f09_mg17"
DRYCORE_COMPSET="FHS94"

os.environ["PATH"]+=":%s"%env.CESM_SCRIPTS