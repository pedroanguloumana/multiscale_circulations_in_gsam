from src.processing import gSAMCoarsenGrid

region = 'northwest_tropical_pacific'
gridsize = 50

gSAMCoarsenGrid().coarsen(region, 'QV', gridsize)
