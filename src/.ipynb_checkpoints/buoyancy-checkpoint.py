import xarray as xr
from metpy.calc import saturation_mixing_ratio
from metpy.units import units
from metpy.constants import *
import numpy as np

def saturation_MSE(temp_da, pressure_da):
    T = temp_da.data * units.degK
    z = temp_da.z.data * units.meter
    p = pressure_da.data * units.hPa
    # p = np.tile(p, (T.shape[1], 1)).T
    # z = np.tile(z, (T.shape[1], 1)).T
    qvs = saturation_mixing_ratio(p, T)

    Lqv_plus_cpT = (water_heat_vaporization*qvs) + (dry_air_spec_heat_press*T)
    MSE = Lqv_plus_cpT + (earth_gravity*z)

    MSE = temp_da.copy(data=MSE) # in J/kg
    
    return MSE