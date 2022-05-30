********
Examples
********

Run Simulations
===============
Here are few examples on how to run Aquaplanets & Drycore simulations and analyse the output.

Running an aquaplanet simulation with a disk type anomaly:

.. code-block:: bash

    python run_pipeline.py -anomaly_type disk -aqua -anomaly_lat 20.0

Running a drycore simulation with a disk type anomaly:

.. code-block:: bash

    python run_pipeline.py -anomaly_type disk -drycore -anomaly_lat 20.0

To rebuild the case append the -rebuild flag:

.. code-block:: bash

    python run_pipeline.py -anomaly_type disk -drycore -rebuild -anomaly_lat 20.0

The default for the drycore anomaly is constant with height. Can also specify -surface or -lapse_rate:

.. code-block:: bash

    python run_pipeline.py -anomaly_type disk -drycore -rebuild -anomaly_lat 20.0 -surface

Run the drycore control case:

.. code-block:: bash

    python run_pipeline.py -control -drycore -rebuild

Run the aquaplanet control case:

.. code-block:: bash

    python run_pipeline.py -control -aqua -rebuild


Visualization
=============

Make gif with specific field:

.. code-block:: bash

    python postprocessing/plot_field.py -infile <file> -field <field> -gif

Plot time average:

.. code-block:: bash

    python postprocessing/plot_field.py -infile <file> -field <field> -avg