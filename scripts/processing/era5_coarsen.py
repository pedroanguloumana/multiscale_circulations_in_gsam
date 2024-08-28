from src.processing import ERA5CoarsenGrid

region = 'northwest_tropical_pacific'
res = 2
variable = 'w'
ERA5CoarsenGrid().coarsen(region, res, variable)
