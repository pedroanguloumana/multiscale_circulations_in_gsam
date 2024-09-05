from src.processing import gSAMCoarsenGrid

region = 'northwest_tropical_pacific'
gridsize = 100

gSAMCoarsenGrid().coarsen(region, 'W', gridsize)
gSAMCoarsenGrid().coarsen(region, '2D', gridsize)
