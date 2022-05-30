"""Inject anomaly"""
import os
import sys

from idealplanets import inject_argparse
from idealplanets.environment import EnvironmentConfig
from idealplanets.preprocessing import anomaly_value
from idealplanets.utilities import open_file

if __name__ == '__main__':

    parser = inject_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    if args.data_dir is None:
        args.data_dir = config.CESM_DATA_DIR
    if args.sst_file is None:
        args.sst_file = config.BASE_SST_FILE
    if args.topo_file is None:
        args.topo_file = config.BASE_TOPO_FILE
    if args.tref_file is None:
        args.tref_file = config.BASE_TREF_FILE
    if args.sst_outfile is None:
        args.sst_outfile = os.path.splitext(config.BASE_SST_FILE)[0]
        args.sst_outfile += "_anomaly.nc"
    if args.topo_outfile is None:
        args.topo_outfile = os.path.splitext(config.BASE_TOPO_FILE)[0]
        args.topo_outfile += "_anomaly.nc"
    if args.tref_outfile is None:
        args.tref_outfile = os.path.splitext(config.BASE_TREF_FILE)[0]
        args.tref_outfile += "_anomaly.nc"

    squared_radius = (args.anomaly_radius)**2

    if args.aqua:
        basefile = args.data_dir + '/' + args.sst_file
        outfile = args.data_dir + '/' + args.sst_outfile
        f = open_file(basefile, 'r')
        data = f.variables['SST_cpl'].get_value()

    elif args.drycore:
        basefile = args.data_dir + '/' + args.tref_file
        outfile = args.data_dir + '/' + args.tref_outfile
        f = open_file(basefile, 'r')
        data = f.variables['tref'].get_value()

    elif args.drycore_topo:
        basefile = args.data_dir + '/' + args.topo_file
        outfile = args.data_dir + '/' + args.topo_outfile
        f = open_file(basefile, 'r')
        data = f.variables['PHIS'].get_value()

        # we assume a temp anomaly coresponds to a change
        # in phi according to dT/dz = -mg/R (gamma-1)/gamma,
        # the dry adiabatic lapse rate
        # args.max_anomaly*=-1000.0

        # lets just pass topo anomaly as km
        args.max_anomaly *= 9.8 * 1000.0

    else:
        print("Select valid case for anomaly injection")
        sys.exit()

    lats = f.variables['lat'].get_value()
    lons = f.variables['lon'].get_value()
    f.close()

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            value = anomaly_value(args.max_anomaly, squared_radius, lon,
                                  args.anomaly_lon, lat, args.anomaly_lat)
            if args.aqua:
                data[:, i, j] += value
            elif args.drycore:
                if args.lapse_rate:
                    for k in range(len(data[0, :, 0, 0])):
                        lapse_rate = value / (len(data[0, :, 0, 0]) - 1)
                        data[:, k, i, j] += k * lapse_rate
                elif args.surface:
                    data[:, -1, i, j] += value
                else:
                    data[:, :, i, j] += value

    os.system('cp %s %s' % (basefile, outfile))
    f = open_file(outfile, 'w')
    print("**Injecting anomaly: %s**" % (outfile))

    if args.aqua:
        f.variables['SST_cpl'].assign_value(data)
    if args.drycore:
        f.variables['tref'].assign_value(data)
    if args.drycore_topo:
        f.variables['PHIS'].assign_value(data)
    f.close()
