#!/bin/bash

echo "Downloading and building CESM"

python scripts/init_cesm.py

echo "Generating base files for heat anomaly injections"

python scripts/init_basefile.py -aqua
python scripts/init_basefile.py -drycore
python scripts/init_basefile.py -drycore_topo
