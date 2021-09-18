import idealplanets.environment as env

import os

cmd="git clone https://github.com/escomp/cesm.git %s" %(env.MY_CESM_DIR)
cmd+="; cd %s" %(env.MY_CESM_DIR)
cmd+="; git checkout release-cesm2.0.0"
cmd+="; ./manage_externals/checkout_externals"

os.system(cmd)
