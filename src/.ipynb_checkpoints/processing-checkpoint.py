# 

from src.configs import ProjectConfigs, gSAMConfigs, ERA5Configs
from glob import glob
import numpy as np
from itertools import product
import os
import xarray as xr
import xeofs as xe
from cdo import *
class MoistureSpaceGrids:
    """
    Class for making moisture space versions of grids.
    """
    def __init__(self, region, gridsize):
        self.region = region
        self.gridsize = gridsize
    
    def _get_variable_files(self, variable):
        variable_files = sorted(glob(f'{gSAMConfigs().native_var_dir(self.region, variable)}/*.nc'))
        return(variable_files)

    def _get_matching_surface_files(self, variable_files):
        variable_file_times = [f.split('/')[-1].split('_')[4] for f in variable_files]
        surface_files = self._get_variable_files('2D')
        surface_file_times = [f.split('/')[-1].split('_')[4] for f in surface_files]
        matching_surface_files = []
        for vft in variable_file_times:
            matching_idx = np.where(vft in surface_file_times)[0]
            assert(len(matching_idx==1))
            matching_surface_files.append(surface_files[matching_idx.item()])
        return(matching_surface_files)

    def _compute_saturation_fraction(self, surface_file_name):
        with xr.open_dataset(surface_file_name) as f:
            return (f.PW / f.PWS).rename('saturation_fraction')

    def _generate_grid_lonlat_slices(self, nlon, nlat):
        lon_slices = [slice(i * self.gridsize, (i + 1) * self.gridsize) for i in range(nlon // self.gridsize)]
        lat_slices = [slice(i * self.gridsize, (i + 1) * self.gridsize) for i in range(nlat // self.gridsize)]
        return({'lon_slices': lon_slices, 'lat_slices': lat_slices})

    def _sort_grid_by_satfrac(self, grid_var, grid_satfrac):
        stack_var = grid_var.stack(column=('lat', 'lon', 'time'))
        stack_satfrac = grid_satfrac.stack(column=('lat', 'lon', 'time'))
        sorted_var = stack_var.sortby(stack_satfrac)
        sorted_var = sorted_var.drop_vars(('lat', 'lon')).assign_coords({'column': np.linspace(0, 1, sorted_var.column.size)})
        return(sorted_var)

    def _filename_to_save(self, lon_index, lat_index, var_filename):
        fn = f"satfrac_sorted.lon_{lon_index}.lat_{lat_index}.{os.path.basename(var_filename)}"
        return(fn)

    def make_moisture_space_grid(self, variable):
        variable_files = self._get_variable_files(variable)
        surface_files = self._get_matching_surface_files(variable_files)
        out_dir = f'{gSAMConfigs().moisture_space_var_dir(self.region, variable, self.gridsize)}'
        os.makedirs(out_dir, exist_ok=True)
        for vi, (var_file, surf_file) in enumerate(zip(variable_files, surface_files)):
            satfrac = self._compute_saturation_fraction(surf_file)
            var_ds = xr.open_dataset(var_file)
            grid_slices = self._generate_grid_lonlat_slices(satfrac.lon.size, satfrac.lat.size)
            for loni, lon_slice in enumerate(grid_slices['lon_slices']):
                for lati, lat_slice in enumerate(grid_slices['lat_slices']):
                    print(f'Processing File {vi+1} of {len(variable_files)} :: lon {loni+1}/{len(grid_slices["lon_slices"])} :: lat {lati+1}/{len(grid_slices["lat_slices"])}')
                    filename_out = f'/{self._filename_to_save(loni, lati, var_file)}'
                    if os.path.exists(out_dir + filename_out):
                        print('File exists! Skipping ...')
                        continue
                    grid_slice = {'lon': lon_slice, 'lat': lat_slice}
                    grid_var = var_ds.isel(grid_slice)
                    grid_satfrac = satfrac.isel(grid_slice)
                    sorted_var = self._sort_grid_by_satfrac(grid_var, grid_satfrac)
                    sorted_var.to_netcdf(out_dir + filename_out)
    
    
    def _compute_theta(self, pcs):
        theta = np.arctan2(pcs.sel(mode=2), pcs.sel(mode=1))
        return(theta)

    def _compute_phase(self, theta):
        p = np.floor(np.mod((np.array(theta)+(np.pi/8))/(np.pi/4) + 4, 8))+1
        return(theta.copy(data=p))

    def _compute_r(self, pcs):
        r2 = pcs.sel(mode=2)**2 + pcs.sel(mode=1)**2
        return(r2**1/2)

    def _get_moisturespace_filename(self, region, var, gridsize, lati, loni, time):
        fn_pattern = f'{gSAMConfigs().moisture_space_var_dir(region, var, gridsize)}/satfrac_sorted.lon_{loni}.lat_{lati}*{time}_*.nc'
        file = glob(fn_pattern)
        assert(len(file)==1)
        return(file[0])
        
    def _get_moisturespace_composite_name(self, var, phase):
        return f'{ProjectConfigs().project_root_dir}/data/moisture_space_composite.{var}.phase{phase:.0f}.{self.region}.nc'
    
    def composite_moisture_grids(self, variable, rmin=0.5):
        pcs_file = f'{ProjectConfigs().project_root_dir}/data/gsam.pcs.{self.region}.massflux.50pix.nc'
        pcs = xr.open_dataarray(pcs_file)
        pcs = pcs/pcs.std(('lat', 'lon', 'time'))
        theta = self._compute_theta(pcs)
        phase = self._compute_phase(theta)
        r = self._compute_r(pcs)
        phase = phase.where(r>rmin, other=0, drop=False)

        for p in [1,2,3,4,5,6,7,8]:
            time_idx, lat_idx, lon_idx = np.where(phase==p)
            time_string = [phase.time[ti].dt.strftime('%Y%m%d%H%M%S').item() for ti in time_idx]
            fnames = [self._get_moisturespace_filename(self.region, variable, self.gridsize, lati, loni, time) for lati, loni, time in zip(lat_idx, lon_idx, time_string)]
            print(f'Concating grid from Phase {p}...')
            phase_data = xr.concat([xr.open_dataset(_) for _ in fnames], dim='observations').mean('observations')
            out_fn = self._get_moisturespace_composite_name(variable, p)

            print(f'Saving {out_fn} ...')
            phase_data.to_netcdf(out_fn)
            # phase_data = (phase_data - phase_data.mean('column'))
            # out_fn = _get_composite_out_file(region, gridsize, p)
            # print('Saving ...')
            # circulation = phase_data.cumsum('column').to_netcdf(out_fn)


    def composite_moisture_circulation(self, rmin=0.5):
        pcs_file = f'{ProjectConfigs().project_root_dir}/data/gsam.pcs.{self.region}.massflux.50pix.nc'
        pcs = xr.open_dataarray(pcs_file)
        pcs = pcs/pcs.std(('lat', 'lon', 'time'))
        theta = self._compute_theta(pcs)
        phase = self._compute_phase(theta)
        r = self._compute_r(pcs)
        phase = phase.where(r>rmin, other=0, drop=False)

        for p in [1,2,3,4,5,6,7,8]:
            time_idx, lat_idx, lon_idx = np.where(phase==p)
            time_string = [phase.time[ti].dt.strftime('%Y%m%d%H%M%S').item() for ti in time_idx]
            fnames = [self._get_moisturespace_filename(self.region, 'W', self.gridsize, lati, loni, time) for lati, loni, time in zip(lat_idx, lon_idx, time_string)]
            print(f'Concating grid from Phase {p}...')
            phase_data = xr.concat([xr.open_dataset(_) for _ in fnames], dim='observations')
            phase_data = phase_data - phase_data.mean('column')
            phase_data = phase_data.cumsum('column')
            out_fn = self._get_moisturespace_composite_name('circulation', p)

            print(f'Saving {out_fn} ...')
            phase_data.to_netcdf(out_fn)










class gSAMCoarsenGrid:
    def _get_variable_files(self, region, variable):
        variable_files = sorted(glob(f'{gSAMConfigs().native_var_dir(region, variable)}/*.nc'))
        return(variable_files)
    def coarsen(self, region, variable, gridsize):
        var_files = self._get_variable_files(region, variable)
        out_dir = gSAMConfigs().coarse_var_dir(region, variable, gridsize)
        os.makedirs(out_dir, exist_ok=True)
        coarsen_dict = {'lat': gridsize, 'lon': gridsize}
        for i, vf in enumerate(var_files):
            print(f'Coarsening File {i+1} of {len(var_files)} ...')
            out_path = f'{out_dir}/coarsened_{gridsize:.0f}pix.{os.path.basename(vf)}'
            xr.open_dataset(vf).coarsen(coarsen_dict).mean().to_netcdf(out_path)
            print(f'Saved to {out_path}')

class ERA5CoarsenGrid:
    def _get_target_grid(self, region, degs):
        return(f'{ERA5Configs().cdo_remap_grid_file(region, degs)}')
    def _get_input_files(self, region, variable):
        return sorted(glob(f'{ERA5Configs().hourly_0p25_dir(variable)}/*.nc'))
    def _get_output_dir(self, variable, degs):
        return f'{ERA5Configs().hourly_coarse_dir(variable, degs)}'

    def coarsen(self, region, degs, variable):
        cdo = Cdo()
        grid_file = ERA5Configs().cdo_remap_grid_file(region, degs)
        input_files = self._get_input_files(region, variable)
        output_dir = self._get_output_dir(variable, degs)
        os.makedirs(output_dir, exist_ok=True)

        for f in input_files:
            output_file = output_dir + f'/coarsened.{os.path.basename(f)}'
            cdo.remapcon(grid_file, input=f, output=output_file)
    
class VerticalEOFs:
    def _get_merged_variable_file(self, region, variable, gridsize):
        variable_files = sorted(glob(f'{gSAMConfigs().coarse_var_dir(region, variable, gridsize)}/merged.nc'))
        return(variable_files)
    
    def gsam_massflux_eofs(self, region, gridsize):
        input_file = gSAMConfigs().coarse_var_dir(region, 'W', gridsize)+'/merged.nc'
        ref_data = xr.open_dataset(gSAMConfigs().reference_file)
        data = xr.open_dataset(input_file)['W']*ref_data.rho
        print('Computing EOFs and PCs ...')
        model = xe.models.EOF(n_modes=10, center=True)
        del model.attrs['solver_kwargs']
        model.fit(data, ('lat', 'lon', 'time'))
        print('Saving output ...')
        out_dir = f'{ProjectConfigs().project_root_dir}/data'
        breakpoint()
        assert(os.path.exists(out_dir))
        model.components().to_netcdf(out_dir + f'/gsam.eofs.{region}.massflux.{gridsize:.0f}pix.nc')
        model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/gsam.pcs.{region}.massflux.{gridsize:.0f}pix.nc')

    def era5_massflux_eofs(self, region, degs):
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
        breakpoint()
        assert(os.path.exists(out_dir))
        model.components().to_netcdf(out_dir + f'/era5.eofs.{region}.massflux.{degs:.0f}deg.nc')
        model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/era5.pcs.{region}.massflux.{degs:.0f}deg.nc')

    def gsam_massflux_eofs_era5_levels(self, region, gridsize):
        input_file = gSAMConfigs().coarse_var_dir(region, 'W', gridsize)+'/merged.nc'
        ref_data = xr.open_dataset(gSAMConfigs().reference_file)
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
        breakpoint()
        assert(os.path.exists(out_dir))
        model.components().to_netcdf(out_dir + f'/gsam_era5_levels.eofs.{region}.massflux.{gridsize:.0f}pix.nc')
        model.scores(normalized=False).unstack().to_netcdf(out_dir + f'/gsam_era5_levels.pcs.{region}.massflux.{gridsize:.0f}pix.nc')
