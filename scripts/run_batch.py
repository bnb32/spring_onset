"""Run cesm in batch"""
import os

from idealplanets import run_batch_argparse
from idealplanets.environment import EnvironmentConfig


if __name__ == '__main__':
    parser = run_batch_argparse()
    args = parser.parse_args()

    args.anomaly_lat = args.anomaly_lat_min
    case = args.case + '_' + args.anomaly_type + '_lat%s_lon%s'
    config = EnvironmentConfig(args.config)

    if args.sims:
        while args.anomaly_lat <= args.anomaly_lat_max:

            pipeline_cmd = 'python %s/run_pipeline.py -anomaly_type %s '
            pipeline_cmd += '-anomaly_radius_squared %s -max_anomaly %s '
            pipeline_cmd += '-anomaly_lat %s -anomaly_lon %s'
            pipeline_cmd = pipeline_cmd % (config.MAIN_DIR, args.anomaly_type,
                                           args.anomaly_radius_squared,
                                           args.max_anomaly, args.anomaly_lat,
                                           args.anomaly_lon)
            os.system(pipeline_cmd)
            args.anomaly_lat += args.anomaly_lat_increment
