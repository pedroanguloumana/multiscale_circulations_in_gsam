from src.processing import MoistureSpaceGrids

region = 'northwest_tropical_pacific'
gridsize = 50
rmin = 0.5
grid = MoistureSpaceGrids(region=region, gridsize=gridsize)
grid.composite_moisture_grids('buoyancy', rmin)
# grid.composite_moisture_grids('QC', rmin)
# grid.composite_moisture_grids('TABS', rmin)
# grid.composite_moisture_grids('QI', rmin)
# grid.composite_moisture_grids('QRAD', rmin)


# grid.composite_moisture_circulation(rmin)

# region = 'northwest_tropical_pacific'
# variable = 'W'
# rmin = 0.5
# MoistureSpaceGrids(
#     region=region, 
#     gridsize=50
# ).composite_moisture_circulation(
#     rmin=rmin
# )