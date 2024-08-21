import xarray as xr
from src.configs import Configs
from glob import glob

def _construct_moisture_space():
    


def main():
    configs = Configs('tropical_nw_pacific')
    surf_files = glob(configs.get_gsam_native_var_dir('2D')+'/*.nc')
    
    

