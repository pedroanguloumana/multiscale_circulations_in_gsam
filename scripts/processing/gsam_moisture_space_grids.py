import src.configs as configs
from src.processing import MoistureSpaceGrids

region = 'tropical_nw_pacific'
variable = 'QV'
gridsize = 50

moisture_space_grids = MoistureSpaceGrids(region, gridsize, variable)
moisture_space_grids.make_moisture_space_grid()