from src.processing import MoistureSpaceGrids

region = 'northwest_tropical_pacific'
gridsize = 50

moisture_space_grids = MoistureSpaceGrids(region, gridsize)
moisture_space_grids.make_moisture_space_grid(variable='QI')
moisture_space_grids.make_moisture_space_grid(variable='2D')
moisture_space_grids.make_moisture_space_grid(variable='QV')
moisture_space_grids.make_moisture_space_grid(variable='QRAD')