## Methods for injesting data
from src.configs import gSAMConfigs, ERA5Configs
from glob import glob
import os
import pandas as pd
import xarray as xr
from cdo import *
class AnalysisRegion:
    def __init__(self, region_name, index_box):
        self._name = region_name
        self._index_box = index_box

    @property
    def name(self):
        return self._name
   
    @property
    def index_box(self):
        return self._index_box

    @index_box.setter
    def index_box(self, new_index_box):
        self._index_box = new_index_box

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
            file_time = self._get_file_time(vf)
            if file_time < pd.Timestamp('2020-02-01'):
                continue
            region_da = xr.open_dataset(vf).isel(region.index_box)
            region_da = region_da.drop_vars('time').assign_coords(time=('time', [self._get_file_time(vf)]))
            out_dir = f'{gSAMConfigs().native_var_dir(region.name, variable)}'
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f'{region.name}.{os.path.basename(vf)}'
            print(f'Processing {output_filename} ...')
            region_da.to_netcdf(os.path.join(out_dir, output_filename))
            print(f'Completed processing {output_filename}')

    def _subset_2D_gsam_region(self, region: AnalysisRegion, variable: str):
        var_files = sorted(glob(f'{gSAMConfigs().raw_2D_dir}/DYAMOND2_9216x4608x74_10s_4608_*.2D_atm.nc'))
        assert len(var_files) > 0, f"No files found for variable {variable} in {gSAMConfigs().raw_3D_dir}"
        
        # Loop over files and pull out the region
        for vf in var_files:
            file_time = self._get_file_time(vf)
            if ((file_time.minute)!=0) or (file_time.hour%3!=0):
                continue
            if file_time < pd.Timestamp('2020-02-01'):
                continue
            region_da = xr.open_dataset(vf).isel(region.index_box)
            region_da = region_da.drop_vars('time').assign_coords(time=('time', [self._get_file_time(vf)]))
            out_dir = f'{gSAMConfigs().native_var_dir(region.name, variable)}'
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f'{region.name}.{os.path.basename(vf)}'
            print(f'Processing {output_filename} ...')
            region_da.to_netcdf(os.path.join(out_dir, output_filename))
            print(f'Completed processing {output_filename}')

class ERA5Injestion:
    def _get_era5_pl_var_file_from_date(self, target_date, var):
        year, month = target_date.year, target_date.month
        month_dir = ERA5Configs().raw_pl_dir(year, month)
        day_file = glob(f'{month_dir}/e5.oper.an.pl.*_{var}.*.'+target_date.strftime('%Y%m%d')+f'00_{target_date.strftime("%Y%m%d")}23.nc')
        assert(len(day_file)==1)
        return(day_file[0])

    def subset_era5_pl_region(self, region_name: str, date_range: pd.DatetimeIndex, wesn: tuple, variable:str):
        cdo = Cdo()
        for date in date_range:
            print('Processing data from ' + date.strftime('%Y-%m-%d'))
            input_file = self._get_era5_pl_var_file_from_date(date, variable)
            output_file = f'{ERA5Configs().hourly_0p25_dir(variable)}/extracted.{region_name}.{os.path.basename(input_file)}'
            cdo.sellonlatbox(wesn[0], wesn[1], wesn[2], wesn[3], input=input_file, output=output_file)
            print(f'Saved at {output_file}')
    