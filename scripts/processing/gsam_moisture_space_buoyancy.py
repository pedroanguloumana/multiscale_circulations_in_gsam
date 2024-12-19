import os
import xarray as xr
import numpy as np
from metpy.calc import virtual_temperature
from metpy.units import units
from metpy.constants import *
from src.buoyancy import *
from src.plotting import *

t_files = moisture_space_file_list('TABS')
qv_files = moisture_space_file_list('QV')

total_files = len(t_files)
t_files = moisture_space_file_list('TABS')
qv_files = moisture_space_file_list('QV')

total_files = len(t_files)

for i, (tf, qvf) in enumerate(zip(t_files, qv_files), start=1):
    print(f"Processing file {i}/{total_files}: T-file: {os.path.basename(tf)}, QV-file: {os.path.basename(qvf)}")
    # Your processing code goes here

    # Make sure files match
    tf_index = os.path.basename(tf).rfind('_')
    qvf_index = os.path.basename(qvf).rfind('_')
    assert(os.path.basename(tf)[:tf_index] == os.path.basename(qvf)[:qvf_index])


    t = xr.open_dataset(tf)
    qv = xr.open_dataset(qvf)

    t = t.TABS.metpy.convert_units('K')
    q = (1000*qv).QV.metpy.convert_units('dimensionless')  # converted to kg/kg

    tv = virtual_temperature(t, q)
    tv_bar = tv.mean('column')

    b = earth_gravity * (tv-tv_bar) / tv_bar

    b_fname = tf.replace('TABS', 'virtual_buoyancy')
    b.to_netcdf(b_fname)


    ### MSE BASED BUOYANCY ###
    # # compute saturation MSE of driest 80% of columns ('environment')
    # h_sat = saturation_MSE(t.sel(column=slice(None,0.8))).mean('column')

    # # compute MSE of each parcel
    # h = MSE(t, qv)

    # # compute difference as measure of buoyancy
    # b = (h - h_sat).rename('buoyancy')

    # b_fname = tf.replace('TABS', 'buoyancy')
    # b.to_netcdf(b_fname)