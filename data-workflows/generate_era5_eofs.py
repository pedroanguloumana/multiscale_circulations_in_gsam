## Computes the EOFs and PCs of vertical velocity from ERA5 data
## Updated: 8/3/2024

import xarray as xr
import numpy as np
import xeofs as xe
from src.configs import Configs

##########################
## USER PARAMETER BLOCK ##
REGION_NAME = "tropical_nw_pacific"
NUM_MODES = 10
##########################
def main():
    configs = Configs(REGION_NAME)
    input_file = configs.get_era5_2deg_var_file('w')
    data = xr.open_dataset(input_file).squeeze() * (-1/9.81)  # convert to mass flux
    data = data.isel(time=data.time.dt.hour%3==0)  # sample at same frequency as gSAM output saved (3 hourly)
    print('Computing EOFs and PCs ...')
    model = xe.models.EOF(n_modes=NUM_MODES, center=True)
    del model.attrs['solver_kwargs']
    model.fit(data, ('lat', 'lon', 'time'))
    print('Saving output ...')
    model.components().to_netcdf(f"{configs.get_project_root_dir()}/data-output/era5.eofs.{REGION_NAME}.massflux.2deg.nc")
    model.scores(normalized=False).unstack().to_netcdf(f"{configs.get_project_root_dir()}/data-output/era5.pcs.{REGION_NAME}.massflux.2deg.nc")
    print('Done!')
    
if __name__=='__main__':
    main()
