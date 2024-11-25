from src.eof_analysis import *

region = 'northwest_tropical_pacific'
gridsize = 50

# To compare to ERA5, compute EOFs using only ERA5 pressure levels
gsam_massflux_eofs_era5_levels(region, gridsize)
gsam_massflux_eofs(region, gridsize)
