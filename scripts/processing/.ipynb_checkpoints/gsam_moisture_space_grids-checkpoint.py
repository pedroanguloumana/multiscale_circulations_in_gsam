from src.processing import MoistureSpaceGrids

region = 'northwest_tropical_pacific'
gridsize = 50

moisture_space_grids = MoistureSpaceGrids(region, gridsize)
moisture_space_grids.make_moisture_space_grid(variable='QRAD')
moisture_space_grids.make_moisture_space_grid(variable='TABS')
moisture_space_grids.make_moisture_space_grid(variable='VOR')