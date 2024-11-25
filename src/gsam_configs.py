# Configurations for gSAM data

def raw_2D_dir():
    return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_2D"

def raw_3D_dir():
    return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_3D"

def moisture_space_var_dir(region, var, gridsize):
    return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_moisture_space_grids_{gridsize:.0f}pix"

def native_var_dir(region, var):
    return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}"

def coarse_var_dir(region, var, gridsize):
    return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_{gridsize:.0f}pix"

def std_var_dir(region, var, gridsize):
    return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_std_{gridsize:.0f}pix"

def reference_file():
    return "/glade/work/pangulo/gsam_dyamond_winter/gsam_z_p_rho_reference.nc"