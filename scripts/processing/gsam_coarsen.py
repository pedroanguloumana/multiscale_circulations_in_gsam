from src.processing import gSAMCoarsenGridCoarsenGrid

region = 'northwest_tropical_pacific'
variable = 'W'
gridsize = 50

gSAMCoarsenGrid().coarsen(region, variable, gridsize)
