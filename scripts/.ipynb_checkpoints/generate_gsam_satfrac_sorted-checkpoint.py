import xarray as xr
import numpy as np
import os
from src.configs import Configs
from glob import glob
import argparse

def _compute_saturation_fraction(surf_fn):
    with xr.open_dataset(surf_fn) as surf:
        return surf.PW / surf.PWS

def _sort_grid_by_saturation_fraction(var_ds, sf_ds):
    stack_var = var_ds.stack(column=('lat', 'lon'))
    stack_sf = sf_ds.stack(column=('lat', 'lon'))
    sorted_var = stack_var.sortby(stack_sf)
    column_rank = np.linspace(0, 1, sorted_var.column.size)
    sorted_var = sorted_var.drop_vars(('lat', 'lon')).assign_coords({'column': column_rank})
    return sorted_var

def main(var, gridsize):
    configs = Configs('tropical_nw_pacific')
    out_dir = configs.get_gsam_satfrac_sorted_var_dir(var, gridsize)
    os.makedirs(out_dir, exist_ok=True)

    surf_files = sorted(glob(os.path.join(configs.get_gsam_native_var_dir('2D'), '*.nc')))
    var_files = sorted(glob(os.path.join(configs.get_gsam_native_var_dir('W'), '*.nc')))
    surf_files_times = [f.split('/')[-1].split('_')[4] for f in surf_files]
    var_file_times = [f.split('/')[-1].split('_')[4] for f in var_files]

    for vi, var_file in enumerate(var_files):
        file_idx = np.where(np.isin(surf_files_times, var_file_times[vi]))[0].item()
        surf_file = surf_files[file_idx]
        satfrac = _compute_saturation_fraction(surf_file)

        lon_size, lat_size = satfrac.lon.size, satfrac.lat.size
        assert lon_size % gridsize == lat_size % gridsize == 0

        lon_slices = [slice(i * gridsize, (i + 1) * gridsize) for i in range(lon_size // gridsize)]
        lat_slices = [slice(i * gridsize, (i + 1) * gridsize) for i in range(lat_size // gridsize)]

        for loni, lon_slice in enumerate(lon_slices):
            for lati, lat_slice in enumerate(lat_slices):
                print(f'Processing File {vi+1} of {len(var_files)} :: lon {loni+1}/{len(lon_slices)} :: lat {lati+1}/{len(lat_slices)}')
                slice_dict = {'lon': lon_slice, 'lat': lat_slice}

                grid_satfrac = satfrac.isel(slice_dict).squeeze('time')
                with xr.open_dataarray(var_file).squeeze('time').isel(slice_dict) as grid_var:
                    sorted_var = _sort_grid_by_saturation_fraction(grid_var, grid_satfrac)
                    filename = f'satfrac_sorted.lon_{loni}.lat_{lati}.{os.path.basename(var_file)}'
                    filepath = os.path.join(out_dir, filename)
                    print(f'Saving {filename} to {out_dir} ...')

                    if os.path.isfile(filepath):
                        continue

                    sorted_var.to_netcdf(filepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    parser.add_argument("-var", type=str, required=True, help="Variable to Process")
    parser.add_argument("-gridsize", type=int, required=True, help="Grid size as an integer")
    args = parser.parse_args()
    main(args.var, args.gridsize)