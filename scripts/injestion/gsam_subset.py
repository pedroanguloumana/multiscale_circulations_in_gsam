from src.configs import ProjectConfigs, gSAMConfigs
from src.injestion import AnalysisRegion, gSAMInjestion

########
# Set up the region we want to subset
# Northwest Tropical Pacific
#   * 1000 x 500 pixels (Lon x Lat)
#   * Lat/Lon Bounds
#       - Index bounds: S/N: 2304 to 2804 ;; W/E: 3327 to 4327
#       - Lat/Lon bounds: S/N: 0.01977827 N to 19.145401 N ;; E/W 130.0E to 169.02344 E
########

south_idx = 2304
north_idx = 2804
west_idx  = 3327
east_idx  = 4327
region = AnalysisRegion(
    region_name='northwest_tropical_pacific',
    index_box={
        'lat': slice(south_idx, north_idx),
         'lon': slice(west_idx, east_idx)
         }
    )

gSAMInjestion().subset_gsam_region(region, 'TABS')
gSAMInjestion().subset_gsam_region(region, 'QV')
gSAMInjestion().subset_gsam_region(region, 'QI')
gSAMInjestion().subset_gsam_region(region, 'QRAD')
gSAMInjestion().subset_gsam_region(region, 'VOR')