"""Initialize basefile"""
import os
import sys
import numpy as np

from idealplanets.environment import EnvironmentConfig
from idealplanets import init_basefile_argparse
from idealplanets.utilities import open_file


if __name__ == '__main__':

    parser = init_basefile_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.aqua:
        f = open_file(config.ORIG_SST_FILE, 'r')
        data = f.variables['SST_cpl'].get_value()
        f.close()

        os.system('cp %s %s/%s' % (config.ORIG_SST_FILE, config.CESM_DATA_DIR,
                                   config.BASE_SST_FILE))
        f = open_file(config.CESM_DATA_DIR + '/' + config.BASE_SST_FILE, 'w')
        f.variables['SST_cpl'].assign_value(data)
        f.close()

    elif args.drycore_topo:
        f = open_file(config.ORIG_TOPO_FILE, 'r')
        data = f.variables['PHIS'].get_value()
        lat = f.variables['lat'].get_value()
        lon = f.variables['lon'].get_value()
        f.close()

        os.system('cp %s %s/%s' % (config.ORIG_TOPO_FILE, config.CESM_DATA_DIR,
                                   config.BASE_TOPO_FILE))
        os.system('chmod 644 %s/%s' % (config.CESM_DATA_DIR,
                                       config.BASE_TOPO_FILE))
        avg_phi = np.mean(data)

        for i in range(0, len(lat)):
            for j in range(0, len(lon)):
                data[i, j] = float(0.0)  # avg_phi

        f = open_file(config.CESM_DATA_DIR + '/' + config.BASE_TOPO_FILE, 'w')
        f.variables['PHIS'].assign_value(data)
        f.close()

    elif args.drycore:
        f = open_file(config.ORIG_TREF_FILE, 'r')
        data = f.variables['tref'].get_value()
        lat = f.variables['lat'].get_value()
        lon = f.variables['lon'].get_value()
        lev = f.variables['lev'].get_value()
        f.close()

        os.system('cp %s %s/%s' % (config.ORIG_TREF_FILE, config.CESM_DATA_DIR,
                                   config.BASE_TREF_FILE))
        os.system('chmod 644 %s/%s' % (config.CESM_DATA_DIR,
                                       config.BASE_TREF_FILE))
        avg_tref = np.mean(data)

        f = open_file(config.CESM_DATA_DIR + '/' + config.BASE_TREF_FILE, 'w')
        f.variables['tref'].assign_value(data)
        f.close()

    else:
        print("Select valid case type")
        sys.exit()
