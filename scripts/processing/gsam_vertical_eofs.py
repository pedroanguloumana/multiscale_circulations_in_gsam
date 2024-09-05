from src.processing import VerticalEOFs

region = 'northwest_tropical_pacific'
gridsize = 100

# To compare to ERA5, compute EOFs using only ERA5 pressure levels
VerticalEOFs().gsam_massflux_eofs_era5_levels(region, gridsize)

