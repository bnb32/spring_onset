************
Idealplanets
************

This repo is for running aquaplanet and drycore simulations with CESM on Cheyenne.

Documentation
*************
`<https://bnb32.github.io/spring_onset/>`_

Initialization
**************

After following the installation instructions `here <https://bnb32.github.io/spring_onset/install.html>`_:

Edit environment configuration:

.. code-block:: bash

    cd spring_onset
    cp idealplanets/environment/config.py my_config.py
    vim my_config.json

Configuration can be in either .py or .json format. Follow the required
variables from config.py. Easiest is just to edit the my_config.py file and
not convert to json.

.. code-block:: bash

    cd spring_onset
    bash ./go.sh

This go script kicks off scripts from the scripts directory and requires
the my_config.py file. Pip has trouble installing PyNIO so this package may
need to be installed manually with conda.

Preprocessing
*************

`idealplanets/preprocessing/inject_anomaly.py` is used to inject a heat anomaly or change in phi into an sst file or topo file. This script can inject disk and band type heat anomalies. Parameters are specified through the command line using the `argparse` module.

Postprocessing
**************

`idealplanets/postprocessing/plot_field.py` is used to visualize output from the aquaplanet simulations.

Simulation
**********

`.F90` files from `cesm_mods` need to be copied into `$CASEDIR/SourceMods/src.cam` and `namelist_definition.xml` needs to be in `$CESM/components/cam/bld/namelist_files/`

`run_cesm.py` runs the aquaplanet/drycore simulation using parameters specified through the `argparse` module.

`run_pipeline.py` injects a heat anomaly, runs the aquaplanet simulation, and can run both visualization scripts. Parameters are again specified through the `argparse` module.

`run_batch.py` can be used to run multiple CESM instances at the same time.
