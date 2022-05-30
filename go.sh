#!/bin/bash

echo "Downloading and building CESM"

python scripts/init_cesm.py -config my_config.py

echo "Generating base files for heat anomaly injections"

python scripts/init_basefile.py -aqua -config my_config.py
python scripts/init_basefile.py -drycore -config my_config.py
python scripts/init_basefile.py -drycore_topo -config my_config.py
