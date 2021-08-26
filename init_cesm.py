import os

cmd="git clone https://github.com/escomp/cesm.git ../my_cesm"
cmd+="; cd ../my_cesm"
cmd+="; git checkout release-cesm2.0.0"
cmd+="; ./manage_externals/checkout_externals"

os.system(cmd)
