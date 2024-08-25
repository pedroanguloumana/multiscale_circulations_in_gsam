## Encodes settings (e.g. paths, names, etc.)
class ProjectConfigs:

    @property
    def project_root_dir(self):
        return "/glade/home/u/pangulo/multiscale_circulations_in_gsam"

class gSAMConfigs:
    @property
    def raw_2D_dir(self):
        return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_2D"
    
    @property
    def raw_3D_dir(self):
        return "/glade/campaign/univ/unsb0021/SAM7.7_DYAMOND2/OUT_3D"

    def moisture_space_var_dir(self, region, var, gridsize):
        return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}_moisture_space{gridsize:.0f}pix"

    def native_var_dir(self, region, var):
        return f"/glade/work/pangulo/gsam_dyamond_winter/{region}/{var}"

    @property
    def reference_file(self):
        return f"/glade/work/pangulo/gsam_dyamond_winter/gsam_z_p_rho_reference.nc"