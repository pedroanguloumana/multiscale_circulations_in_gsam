## Encodes settings (e.g. paths, names, etc.)

class Configs:
    def __init__(self, region_name: str):
        self.region_name = region_name
    
    def get_project_root_dir(self) -> str:
        return "~/multiscale_circulations_in_gsam"
        
    def get_gsam_native_var_dir(self, var) -> str:
        return f"/glade/work/pangulo/gsam/{self.region_name}/{var}"

    def get_gsam_coarse_var_file(self, var, coarse_res) -> str:
        return f"/glade/work/pangulo/gsam/{self.region_name}/{var}_{coarse_res}pix/merged.nc"

    def get_era5_2deg_var_file(self, var) -> str:
        return f"/glade/work/pangulo/gsam/{self.region_name}/{var}_{coarse_res}pix/merged.nc"

    def get_cmorph_2deg_file(self) -> str:
        return f"/glade/work/pangulo/cmorph/dyamond_winter/{self.region_name}/2deg/merged.nc"