from src.processing import VerticalEOFs

region = 'northwest_tropical_pacific'
degs = 2

VerticalEOFs().era5_massflux_eofs(region, degs)

