import xarray as xr
import os
from glob import glob
from metpy.calc import saturation_mixing_ratio
from metpy.units import units
from metpy.constants import *
import numpy as np


def moisture_space_file_list(var):
    path = f'/glade/u/home/pangulo/work/gsam_dyamond_winter/northwest_tropical_pacific/{var}_moisture_space_grids_50pix'
    assert(os.path.isdir(path))

    files = np.sort(glob(path+'/satfrac_sorted.*.nc'))
    return files

def saturation_MSE(temp_da):
    '''
    I use MetPy here because computing the saturation mixing ratio is a pain.
    '''
    T = temp_da.TABS.data * units.degK
    z = temp_da.z.data * units.meter
    p = temp_da.p.data * units.hPa
    p = np.tile(p, (T.shape[1], 1)).T
    z = np.tile(z, (T.shape[1], 1)).T
    qvs = saturation_mixing_ratio(p, T)

    Lqv_plus_cpT = (water_heat_vaporization*qvs) + (dry_air_spec_heat_press*T)
    MSE = Lqv_plus_cpT + (earth_gravity*z)

    MSE = temp_da.TABS.copy(data=MSE) # in J/kg
    
    return MSE

def MSE(t, qv):
    T = t.TABS.data * units.degK
    QV = qv.QV.data * units('g/kg')
    z = t.z.data * units.meter
    z = np.tile(z, (T.shape[1], 1)).T
    Lqv_plus_cpT = (water_heat_vaporization*QV) + (dry_air_spec_heat_press*T)
    MSE = Lqv_plus_cpT + (earth_gravity*z)
    MSE = t.TABS.copy(data=MSE) # in J/kg
    return MSE 
    

