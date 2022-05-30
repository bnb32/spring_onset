"""Environment configuration"""
import os
import json
import importlib.util
import sys


class EnvironmentConfig:
    """Class storing configuration parameters"""

    USERNAME = None
    NETID = None
    PROJECT_CODE = None
    MAIN_DIR = '/tmp'

    MY_CESM_DIR = MAIN_DIR + '/my_cesm'
    POST_PROC_DIR = MAIN_DIR + '/idealplanets/postprocessing/'
    PRE_PROC_DIR = MAIN_DIR + '/idealplanets/preprocessing/'
    SCRATCH_DIR = f'/glade/scratch/{USERNAME}/'
    CIME_OUTPUT_ROOT = SCRATCH_DIR + '/cases/'
    CESM_DATA_DIR = SCRATCH_DIR + '/cesm_data/'
    CESM_SCRIPTS = MY_CESM_DIR + '/cime/scripts/'
    CESM_CAM_OUT_DIR = SCRATCH_DIR + '/archive/%s/atm/hist/'
    ORIG_DATA_DIR = '/glade/p/cesmdata/cseg/inputdata/'
    ORIG_TOPO_DIR = ORIG_DATA_DIR + '/atm/cam/topo/'
    ORIG_TREF_DIR = MAIN_DIR + '/trefread/NCL/output/'
    ORIG_SST_DIR = ORIG_DATA_DIR + '/ocn/docn7/AQUAPLANET/'
    ORIG_TOPO_FILE = ORIG_TOPO_DIR + '/USGS-gtopo30_64x128_c050520.nc'
    ORIG_TREF_FILE = ORIG_TREF_DIR + '/tref_T85L30.nc'
    ORIG_SST_FILE = ORIG_SST_DIR + '/sst_c4aquasom_0.9x1.25_clim.c170512.nc'
    BASE_SST_FILE = 'aqua_sst.nc'
    BASE_TOPO_FILE = 'drycore_topo.nc'
    BASE_TREF_FILE = 'drycore_tref.nc'
    AQUA_RES = "f09_f09_mg17"
    AQUA_COMPSET = "QPC6"
    DRYCORE_RES = "T85z30_T85_mg17"
    DRYCORE_COMPSET = "FHS94"

    def __init__(self, file_name):
        """
        Parameters
        ----------
        file_name : string
            JSON or .py configuration file
        """
        self.file_name = file_name
        self.config_dict = {}
        self.get_config(file_name)
        self.update_env()
        self.init_dirs()

    @staticmethod
    def load_config(file_name):
        """Load config from python file"""
        spec = importlib.util.spec_from_file_location("config", file_name)
        config = importlib.util.module_from_spec(spec)
        sys.modules["config"] = config
        spec.loader.exec_module(config)
        return config

    def get_config(self, file_name=None):
        """Get configuration from file
        Parameters
        ----------
        file_name : string
            Path to configuration file
        Returns
        -------
        RunConfig
            Config class with run time configuration stored in attributes
        """

        if file_name is not None:
            if file_name.split('.')[-1] == 'py':
                config = self.load_config(file_name)
                for k in dir(config):
                    if k.upper() == k:
                        if hasattr(self, k):
                            setattr(self, k, getattr(config, k))
            elif file_name.split('.')[-1] == 'json':
                with open(file_name, 'r') as fh:
                    self.config_dict = json.load(fh)

                for k, v in self.config_dict.items():
                    if hasattr(self, k):
                        setattr(self, k, v)

    def update_env(self):
        """Update path after loading config"""
        os.environ["PATH"] += f":{self.CESM_SCRIPTS}"
        for d in dir(self):
            if d.upper() == d:
                os.environ[d] = getattr(self, d)

    def init_dirs(self):
        """Make project directories"""
        for d in dir(self):
            if 'DIR' in d:
                os.system(f'mkdir -p {d}')
