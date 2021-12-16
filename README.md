# README #

This repo is for running aquaplanet and drycore simulations with CESM on Cheyenne.

**Environment**

Environment variables are defined in `idealplanets/environment.py`.

**Initialize**

```bash
pip install -e .
bash go.sh
```

**Preprocessing**

`idealplanets/preprocessing/inject_anomaly.py` is used to inject a heat anomaly or change in phi into an sst file or topo file. This script can inject disk and band type heat anomalies. Parameters are specified through the command line using the `argparse` module.

**Postprocessing**

`idealplanets/postprocessing/plot_field.py` is used to visualize output from the aquaplanet simulations.

**Simulation**

`.F90` files from `cesm_mods` need to be copied into `$CASEDIR/SourceMods/src.cam` and `namelist_definition.xml` needs to be in `$CESM/components/cam/bld/namelist_files/`

`run_cesm.py` runs the aquaplanet/drycore simulation using parameters specified through the `argparse` module.

`run_pipeline.py` injects a heat anomaly, runs the aquaplanet simulation, and can run both visualization scripts. Parameters are again specified through the `argparse` module. 

`run_batch.py` can be used to run multiple CESM instances at the same time.
