## Encodes settings (e.g. paths, names, etc.)
class ProjectConfigs:

    @property
    def project_root_dir(self):
        return "/glade/u/home/pangulo/multiscale_circulations_in_gsam"

class gSAMConfigs:
    @property
    def raw_2D_dir(self):
        return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_2D"
    
    @property
    def raw_3D_dir(self):
        return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_3D"

    def moisture_space_var_dir(self, region, var, gridsize):
        return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_moisture_space_grids_{gridsize:.0f}pix"

    def native_var_dir(self, region, var):
        return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}"

    def coarse_var_dir(self, region, var, gridsize):
        return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_{gridsize:.0f}pix"
        
    @property
    def reference_file(self):
        return f"/glade/work/pangulo/gsam_dyamond_winter/gsam_z_p_rho_reference.nc"

class ERA5Configs:
    def raw_pl_dir(self, year, month):
        return f"/glade/campaign/collections/rda/data/ds633.0/e5.oper.an.pl/{year:04d}{month:02d}"

    def hourly_0p25_dir(self, region, var):
        return f"/glade/work/pangulo/era5/dyamond_winter/{region}/{var}_hourly_0p25"
    
    def hourly_coarse_dir(self, region, var, degs):
        return f"/glade/work/pangulo/era5/dyamond_winter/{region}/{var}_hourly_{degs:.0f}deg"

    def cdo_remap_grid_file(self, region, degs):
        return f"{ProjectConfigs().project_root_dir}/scripts/processing/{region}_{degs}deg.grid"