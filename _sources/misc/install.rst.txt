Clone repo (recommended for developers)
---------------------------------------

1. from home dir, ``git clone git@github.com:bnb32/spring_onset.git``

2. Create ``idealplanets`` environment and install package
    1) Create a conda env: ``conda create -n idealplanets``
    2) Run the command: ``conda activate idealplanets``
    3) cd into the repo cloned in 1.
    4) prior to running ``pip`` below, make sure the branch is correct (install
       from main!)
    5) Install ``idealplanets`` and its dependencies by running:
       ``pip install .`` (or ``pip install -e .`` if running a dev branch
       or working on the source code)
    6) Install PyNIO with conda (``conda install pynio``)