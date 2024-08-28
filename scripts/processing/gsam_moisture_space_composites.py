from src.processing import MoistureSpaceGrids

region = 'northwest_tropical_pacific'
variable = 'W'
rmin = 0.5
MoistureSpaceGrids().composite_moisture_grids(
    region=region, 
    variable=variable, 
    rmin=rmin
)

