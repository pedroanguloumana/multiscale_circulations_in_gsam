from glob import glob
import xarray as xr
import xeofs as xe 
import os
from src.project_configs import *
from src.gsam_configs import *
from src.plotting import *
from src.configs import ERA5Configs, ProjectConfigs

def _get_merged_variable_file(region, variable, gridsize):
    variable_files = sorted(glob(f'{coarse_var_dir(region, variable, gridsize)}/merged.nc'))
    return(variable_files)

def gsam_massflux_eofs(region, gridsize):
    input_file = coarse_var_dir(region, 'W', gridsize)+'/merged.nc'
    ref_data = load_gsam_ref_data()
    data = xr.open_dataset(input_file)['W']*ref_data.rho
    print('Computing EOFs and PCs ...')
    model = xe.models.EOF(n_modes=10, center=True)
    del model.attrs['solver_kwargs']
    model.fit(data, ('lat', 'lon', 'time'))
    print('Saving output ...')
    out_dir = f'{ProjectConfigs().project_root_dir}/data'
    assert(os.path.exists(out_dir))
    model.explained_variance_ratio().to_netcdf(out_dir + f'/gsam.explained_variance_ratio.{region}.massflux.{gridsize:.0f}pix.nc')
    model.components().to_netcdf(out_dir + f'/gsam.eofs.{region}.massflux.{gridsize:.0f}pix.nc')
    model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/gsam.pcs.{region}.massflux.{gridsize:.0f}pix.nc')

def era5_massflux_eofs(region, degs):
    input_file = f'{ERA5Configs().hourly_coarse_dir(region, "w", degs)}/merged.nc'
    # mass flux
    data = xr.open_dataset(input_file)['W'] * (-1/9.81) 
    # only look at 3 hourly data
    data = data.isel(time=data.time.dt.hour%3==0)
    print('Computing EOFs and PCs ...')
    model = xe.models.EOF(n_modes=10, center=True)
    del model.attrs['solver_kwargs']
    model.fit(data, ('lat', 'lon', 'time'))
    print('Saving output ...')
    out_dir = f'{ProjectConfigs().project_root_dir}/data'
    assert(os.path.exists(out_dir))
    model.explained_variance_ratio().to_netcdf(out_dir + f'/era5.explained_variance_ratio.{region}.massflux.{degs:.0f}pix.nc')
    model.components().to_netcdf(out_dir + f'/era5.eofs.{region}.massflux.{degs:.0f}deg.nc')
    model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/era5.pcs.{region}.massflux.{degs:.0f}deg.nc')

def gsam_massflux_eofs_era5_levels(region, gridsize):
    input_file = input_file = coarse_var_dir(region, 'W', gridsize)+'/merged.nc'
    ref_data = load_gsam_ref_data()
    data = xr.open_dataset(input_file)['W']*ref_data.rho
    # move gsam data to pressure coordinates and interp
    data = data.assign_coords({'z': ref_data.p}).rename({'z': 'level'})
    era5_p_levels = xr.open_dataarray(f'{ProjectConfigs().project_root_dir}/data/era5.eofs.northwest_tropical_pacific.massflux.2deg.nc')['level']
    data = data.interp(level=era5_p_levels)

    print('Computing EOFs and PCs ...')
    model = xe.models.EOF(n_modes=10, center=True)
    del model.attrs['solver_kwargs']
    model.fit(data, ('lat', 'lon', 'time'))
    print('Saving output ...')
    out_dir = f'{ProjectConfigs().project_root_dir}/data'
    assert(os.path.exists(out_dir))
    model.explained_variance_ratio().to_netcdf(out_dir + f'/gsam_era5_levels.explained_variance_ratio.{region}.massflux.{gridsize:.0f}pix.nc')
    model.components().to_netcdf(out_dir + f'/gsam_era5_levels.eofs.{region}.massflux.{gridsize:.0f}pix.nc')
    model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/gsam_era5_levels.pcs.{region}.massflux.{gridsize:.0f}pix.nc')
