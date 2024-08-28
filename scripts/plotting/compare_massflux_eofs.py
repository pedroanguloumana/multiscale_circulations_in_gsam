import xarray as xr
import matplotlib.pyplot as plt
from src.configs import ProjectConfigs

# Load the data

def main():
    root_config = ProjectConfigs().project_root_dir
    gsam_eofs = xr.open_dataarray(f'{root_config}/data/gsam.pcs.northwest_tropical_pacific.massflux.50pix.nc')
    era5_eofs = xr.open_dataarray(f'{root_config}/data/era5.pcs.northwest_tropical_pacific.massflux.2deg.nc')
    fig, axs = plt.subplots(ncols=2, figsize=(7,4), constrained_layout=True)
    era5_eofs.sel(mode=1).plot(ax=axs[0], y='level', color='k', label='ERA5')
    era5_eofs.sel(mode=2).plot(ax=axs[1], y='level', color='k', label='ERA5')
    gsam_eofs.sel(mode=1).plot(ax=axs[0], y='level', color='b', label='gSAM')
    gsam_eofs.sel(mode=2).plot(ax=axs[1], y='level', color='b', label='gSAM')
    axs[0].set_title('EOF 1')
    axs[1].set_title('EOF 2')
    for ax in axs:
        ax.legend()
        ax.invert_yaxis()
        ax.set_ylim(1000, 100)
        ax.set_xlabel('Normalized Vert Mass Flux')

    plt.savefig(f'{root_config}/figures/gsam_era5_massflux_eofs.pdf', format='pdf')
if __name__=='__main__':
    main()