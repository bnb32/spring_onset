"""Initialize CESM"""
import os

from idealplanets.environment import EnvironmentConfig
from idealplanets import init_cesm_argparse


if __name__ == '__main__':

    parser = init_cesm_argparse()
    args = parser.parse_args()
    config = EnvironmentConfig(args.config)

    cmd = "git clone https://github.com/escomp/cesm.git %s"
    cmd = cmd % (config.MY_CESM_DIR)
    cmd += "; cd %s" % (config.MY_CESM_DIR)
    cmd += "; git checkout release-cesm2.0.0"
    cmd += "; ./manage_externals/checkout_externals"

    os.system(cmd)
