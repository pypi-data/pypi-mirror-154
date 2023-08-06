source .env/bin/activate
unset CONDA_PREFIX
python3 -m pip install cameo_ocean --upgrade
python3 -c 'import cameo_ocean;print(cameo_ocean.py_multiply(10,3))'
