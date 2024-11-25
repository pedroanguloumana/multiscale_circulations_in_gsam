# Methods for handling moisture-sorted data
from glob import glob
def fetch_moisture_sorted_grids(var, lat_indicies, lon_indicies, times):
    path = f'/glade/u/home/pangulo/work/gsam_dyamond_winter/northwest_tropical_pacific/{var}_moisture_space_grids_50pix'
    all_files = glob(f'{path}/satfrac_sorted.*.nc')
    assert(len(all_files)>0)

    # get lat inidicies of files
    