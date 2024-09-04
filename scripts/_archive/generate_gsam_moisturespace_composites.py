import xarray as xr
import numpy as np
from src.configs import Configs
from glob import glob

def _compute_theta(pcs):
    theta = np.arctan2(pcs.sel(mode=2), pcs.sel(mode=1))
    return(theta)

def _compute_r(pcs):
    r2 = pcs.sel(mode=2)**2 + pcs.sel(mode=1)**2
    return(r2**1/2)
    
def _compute_phase_number(theta):
    p = np.floor(np.mod((np.array(theta)+(np.pi/8))/(np.pi/4) + 4, 8))+1
    return(theta.copy(data=p))

def _get_moisturespace_filename(dir, lati, loni, time):
    fn_pattern = f'{dir}/satfrac_sorted.lon_{loni}.lat_{lati}*{time}_*.nc'
    file = glob(fn_pattern)
    assert(len(file)==1)
    return(file[0])

def _get_gsam_pcs(region, gridsize, normalize=True):
    pcs = xr.open_dataarray(f'~/multiscale_circulations_in_gsam/data-output/gsam.pcs.{region}.massflux.{gridsize}pix.nc')
    if normalize:
        pcs = pcs/pcs.std(('lat', 'lon', 'time'))
    return(pcs)
    
def _get_composite_out_file(region, gridsize, phase):
    return(f'~/multiscale_circulations_in_gsam/data-output/gsam.composite_circulation.phase{phase:.0f}.nc')


def main(region, var, gridsize):
    configs = Configs(region)
    pcs = _get_gsam_pcs(region, gridsize, normalize=True)
    theta = _compute_theta(pcs)
    r = _compute_r(pcs)
    phase = _compute_phase_number(theta)
    rho = xr.open_dataset(configs.get_gsam_reference_file()).rho
    # designate grids with r<0.5 as being phase 0
    phase = phase.where(r>0.5, other=0, drop=False)
    moisture_space_dir = configs.get_gsam_satfrac_sorted_var_dir(var, gridsize)
    for p in range(1, 9):
        print(f'Processing Phase {p} ...')
        time_idx, lat_idx, lon_idx = np.where(phase==p)
        fnames = [_get_moisturespace_filename(moisture_space_dir, lati, loni, phase.time[ti].dt.strftime('%Y%m%d%H%M%S').item()) for lati, loni, ti in zip(lat_idx, lon_idx, time_idx)]
        phase_data = xr.concat([xr.open_dataarray(_) for _ in fnames], dim='observations')
        mass_flux = (phase_data - phase_data.mean('column')) * rho
        out_fn = _get_composite_out_file(region, gridsize, p)
        print('Saving ...')
        circulation = mass_flux.cumsum('column').mean('observations').to_netcdf(out_fn)

if __name__=='__main__':
    region = 'tropical_nw_pacific'
    var = 'W'
    gridsize = 50
    main(region, var, gridsize)
