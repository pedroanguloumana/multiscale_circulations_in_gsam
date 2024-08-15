## Computes the EOFs and PCs of vertical velocity from gSAM DYAMOND Winter data, interpolated to ERA5 levels
## Updated: 8/3/2024

import xarray as xr
import numpy as np
import xeofs as xe
import pandas as pd
from src.configs import Configs

##########################
## USER PARAMETER BLOCK ##
REGION_NAME = "tropical_nw_pacific"
NUM_MODES = 10
###########################

def main():
    configs = Configs(REGION_NAME)
    input_file = configs.get_gsam_coarse_var_file('W', 50)  # get merged file with 50x50 coarsening
    ref_data = xr.open_dataset(configs.get_gsam_reference_file())
    data = xr.open_dataset(input_file)
    data = data['W'] * ref_data.rho  # convert to mass flux
    data = data.assign_coords({'time': pd.date_range('20200201', '20200229 21:00:00', freq='3h'), 'z': ref_data.p}).rename({'z': 'p'})
    data = data.interp(p=configs.get_era5_pressure_levels())
    print('Computing EOFs and PCs ...')
    model = xe.models.EOF(n_modes=NUM_MODES, center=True)
    del model.attrs['solver_kwargs']
    model.fit(data, ('lat', 'lon', 'time'))

    print('Saving output ...')
    model.components().to_netcdf(f"{configs.get_project_root_dir()}/data-output/gsam.eofs.{REGION_NAME}.massflux.50pix.nc")
    model.scores(normalized=False).unstack().to_netcdf(f"{configs.get_project_root_dir()}/data-output/gsam.pcs.{REGION_NAME}.massflux.50pix.nc")
    print('Done!')

if __name__=='__main__': 
    main()