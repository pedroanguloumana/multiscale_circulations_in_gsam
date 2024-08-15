## Encodes settings (e.g. paths, names, etc.)
import xarray as xr

class Configs:
    def __init__(self, region_name: str):
        self.region_name = region_name
    
    def get_project_root_dir(self) -> str:
        return "~/multiscale_circulations_in_gsam"

    def get_gsam_native_var_dir(self, var) -> str:
        return f"/glade/work/pangulo/gsam_dyamond_winter/{self.region_name}/{var}"

    def get_gsam_reference_file(self) -> str:
        return "/glade/work/pangulo/gsam_dyamond_winter/gsam_z_p_rho_reference.nc"

    def get_gsam_coarse_var_file(self, var, coarse_res) -> str:
        return f"/glade/work/pangulo/gsam_dyamond_winter/{self.region_name}/{var}_{coarse_res}pix/merged.nc"

    def get_era5_2deg_var_file(self, var) -> str:
        return f"/glade/work/pangulo/era5/dyamond_winter/{self.region_name}/{var}_2deg/merged.nc"

    def get_era5_pressure_levels(self):
        levels = xr.open_dataset(f"/glade/work/pangulo/era5/dyamond_winter/{self.region_name}/w/extracted.{self.region_name}.e5.oper.an.pl.128_135_w.ll025sc.2020022900_2020022923.nc").level
        return(levels)

    def get_cmorph_2deg_file(self) -> str:
        return f"/glade/work/pangulo/cmorph/dyamond_winter/{self.region_name}/2deg/merged.nc"