New Python virtual environment:
    name: salinization
    python: 3.7
    jupyter notebook: 6.0

    conda create --name salinization python=3.7
    
    conda config --set channel_priority strict

    add the following settings into ~/.condarc
        channel_priority: strict
        channels:
            - conda-forge
            - defaults

    conda install jupyter

Packages:
    numpy
    pandas
    seaborn

    geographic support:
        geopandas
        descartes
        earthpy

    excel support:
        openpyxl
        xlrd

    html support:
        conda install lxml html5lib beautifulsoup4

    unidecode
    sqlalchemy
    psycopg2
    luigi
    boto3: conda install --channel conda-forge boto3
    cassandra-driver: conda install -c conda-forge cassandra-driver
    pytest

    scikit-learn
    statsmodels

    Pyramid ARIMA:
        conda install -c alkaline-ml pmdarima (does not work)
        pip install pmdarima

    hdbscan: conda install -c conda-forge hdbscan
    hmmlearn: conda install --channel omnia hmmlearn

    dtreeviz (required pip install):
        conda uninstall python-graphviz
        conda uninstall graphviz
        pip install dtreeviz

    pdpbox (Partial Dependence Plot): conda install -c conda-forge pdpbox

    dask: conda install dask
    dask-ml: conda install --channel conda-forge dask-ml

Luigi:
    run_luigi_tasks.py
        #!/bin/sh
        luigid --background --port 8082 --logdir ./log
        python hello_world.py HelloWorldTask --workers=2

    visualization tool:
        http://localhost:8082

    configurtion file:
        ./luigi.cfg
        or 
        export LUIGI_CONFIG_PATH=staging.luigi.cfg

    wrapper task (luigi.WrapperTask):
        no run() or output() methods
        just requires() method to define required another tasks