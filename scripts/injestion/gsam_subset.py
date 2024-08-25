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

region = AnalysisRegion('northwest_tropical_pacific')
region.set_index_box(
    south_idx = 2304, 
    north_idx = 2804, 
    west_idx  = 3327,
    east_idx  = 4327
)

gSAMInjestion().subset_gsam_region(region, '2D')