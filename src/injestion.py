## Methods for injesting data
from src.configs import gSAMConfigs
from glob import glob
import os
import pandas as pd
import xarray as xr
class AnalysisRegion:
    def __init__(self, region_name):
        self._name = region_name
        self._index_box = {'lat': None, 'lon': None}

    @property
    def name(self):
        return self._name
   
    @property
    def index_box(self):
        return self._index_box

    def set_index_box(self, south_idx, north_idx, west_idx, east_idx):
        self._index_box['lat'] = slice(south_idx, north_idx)
        self._index_box['lon'] = slice(west_idx, east_idx)

class gSAMInjestion:
    def subset_gsam_region(self, region: AnalysisRegion, variable: str):
        if variable == '2D':
            self._subset_2D_gsam_region(region, variable)
        else:
            self._subset_3D_gsam_region(region, variable)

    def _get_file_time(self, filename: str) -> pd.Timestamp:
        filename = os.path.basename(filename)
        time_string = filename.split('_')[4]
        return pd.to_datetime(time_string, format='%Y%m%d%H%M%S')

    def _subset_3D_gsam_region(self, region: AnalysisRegion, variable: str):
        var_files = sorted(glob(f'{gSAMConfigs().raw_3D_dir}/DYAMOND2_9216x4608x74_10s_4608_*_{variable}.atm.3D.nc'))
        assert len(var_files) > 0, f"No files found for variable {variable} in {gSAMConfigs().raw_3D_dir}"
        
        # Loop over files and pull out the region
        for vf in var_files:
            region_da = xr.open_dataset(vf).isel(region.index_box)
            region_da = region_da.drop_vars('time').assign_coords(time=('time', [self._get_file_time(vf)]))
            out_dir = f'{gSAMConfigs().native_var_dir(region.name, variable)}'
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f'{region.name}.{os.path.basename(vf)}'
            region_da.to_netcdf(os.path.join(out_dir, output_filename))
    
    def _subset_2D_gsam_region(self, region: AnalysisRegion, variable: str):
        var_files = sorted(glob(f'{gSAMConfigs().raw_2D_dir}/DYAMOND2_9216x4608x74_10s_4608_*.2D_atm.nc'))
        assert len(var_files) > 0, f"No files found for variable {variable} in {gSAMConfigs().raw_3D_dir}"
        
        # Loop over files and pull out the region
        for vf in var_files:
            file_time = self._get_file_time(vf)
            if ((file_time.minute)!=0) or (file_time.hour%3!=0):
                continue
            region_da = xr.open_dataset(vf).isel(region.index_box)
            region_da = region_da.drop_vars('time').assign_coords(time=('time', [self._get_file_time(vf)]))
            out_dir = f'{gSAMConfigs().native_var_dir(region.name, variable)}'
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f'{region.name}.{os.path.basename(vf)}'
            region_da.to_netcdf(os.path.join(out_dir, output_filename))
            breakpoint()