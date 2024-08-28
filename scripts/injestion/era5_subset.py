from src.configs import ProjectConfigs, ERA5Configs
from src.injestion import ERA5Injestion
import pandas as pd
## Make region we want to analyze
## Northwest tropical pacific
## region = AnalysisRegion(
## index_box={'latitude': slice(0, 19.75, -1), 'longitude': slice(130, 169.75)}
## bounds chosen to give 160x80 grid


region_name = 'northwest_tropical_pacific'
lat_south, lat_north = 0, 20
lon_west,  lon_east  = 130, 170
variable = 'w'
date_range = pd.date_range('2020-02-01', '2020-03-01', freq='1d')


ERA5Injestion().subset_era5_pl_region(
    region_name = region_name,
    date_range = date_range, 
    wesn = (lon_west, lon_east, lat_south, lat_north),
    variable = variable,
)






## Abuse of notation, will use real latitudes of region
# era5_date_range = pd.date_range('2020-02-01', '2020-03-01', freq='3h')



# ERA5Injestion().subset_era5_pl_region(era5_date_range, region, 'w')
# ## TODO: test this code