# 

import src.configs as configs
from glob import glob
import numpy as np
from itertools import product
import os

class MoistureSpaceGrids:
    """
    Class for making moisture space versions of grids.

    """
    def __init__(self, region, gridsize, variable):
        self.region = region
        self.gridsize = gridsize
        self.variable = variable
    
    def _get_variable_files(self, variable):
        variable_files = sorted(glob(f'{configs.gSAMConfigs(self.region).get_gsam_native_var_dir(self.variable)}/*.nc'))
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
        stack_var = grid_var.stack(column=('lat', 'lon'))
        stack_satfrac = grid_satfrac.stack(column=('lat', 'lon'))
        sorted_var = stack_var.sortby(stack_satfrac)
        sorted_var = sorted_var.drop_var(('lat', 'lon').assign_coords({'column': np.linspace(0, 1, sorted_var.column.size)}))
        return(sorted_var)

    def _filename_to_save(self, lon_index, lat_index, var_filename):
        fn = f"satfrac_sorted.lon_{loni}.lat_{lati}.{os.path.basename(var_filename)}"
        return(fn)

    def make_moisture_space_grid(self):
        print('whoa')
        variable_files = self._get_variable_files(self.variable)
        surface_files = self._get_matching_surface_files(variable_files)
        breakpoint()
        for var_file, surf_file in zip(variable_files, surface_files):
            satfrac = self._compute_saturation_fraction(surf_files)
            var_ds = xr.open_dataset(var_file)
            grid_slices = self._generate_grid_lonlat_slices(satfrac.lon.size, satfrac.lat.size)
            for loni, lon_slice in enumerate(grid_slices['lon_slices']):
                for lati, lat_slice in enumerate(grid_slices['lat_slices']):
                    print(f'Processing File {vi+1} of {len(var_files)} :: lon {loni+1}/{len(lon_slices)} :: lat {lati+1}/{len(lat_slices)}')
                    grid_slice = {'lon': lon_slice, 'lat': lat_slice}
                    grid_var = var_ds.isel(grid_slice)
                    grid_satfrac = satfrac.isel(grid_slice)
                    sorted_var = self._sort_grid_by_satfrac(self, grid_var, grid_satfrac)
                    filename_out = f"{configs.gSAMConfigs.get_gsam_moisture_space_var_dir()}/{_filename_to_save(loni, lati, var_file)}"
                    sorted_var.to_netcdf(filename_out)