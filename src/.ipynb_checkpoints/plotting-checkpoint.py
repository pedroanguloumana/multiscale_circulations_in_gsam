# Functions for generating plots
import numpy as np
import xarray as xr
import pandas as pd
from scipy.stats import binned_statistic_2d
from src.project_configs import *

## Loading methods 
def load_gsam_ref_data():
    file = "/glade/u/home/pangulo/work/gsam_dyamond_winter/gsam_z_p_rho_reference.nc"
    return xr.open_dataset(file)
def load_gsam_eofs():
    eof_file = 'gsam.eofs.northwest_tropical_pacific.massflux.50pix.nc'
    eofs = xr.open_dataarray(f'{project_root_dir()}/data/{eof_file}')
    return eofs

def load_gsam_eofs_on_era5_levels():
    eof_file = 'gsam_era5_levels.eofs.northwest_tropical_pacific.massflux.50pix.nc'
    eofs = xr.open_dataarray(f'{project_root_dir()}/data/{eof_file}')
    return eofs

def load_era5_eofs():
    eof_file = 'era5.eofs.northwest_tropical_pacific.massflux.2deg.nc'
    eofs = xr.open_dataarray(f'{project_root_dir()}/data/{eof_file}')
    return eofs
def load_gsam_pcs():
    pc_file = 'gsam.pcs.northwest_tropical_pacific.massflux.50pix.nc'
    pcs = xr.open_dataarray(f'{project_root_dir()}/data/{pc_file}')
    return pcs

def load_gsam_pcs_on_era5_levels():
    pc_file = 'gsam_era5_levels.pcs.northwest_tropical_pacific.massflux.50pix.nc'
    pcs = xr.open_dataarray(f'{project_root_dir()}/data/{pc_file}')
    return pcs

def load_era5_pcs():
    pc_file = 'era5.pcs.northwest_tropical_pacific.massflux.2deg.nc'
    pcs = xr.open_dataarray(f'{project_root_dir()}/data/{pc_file}')
    return pcs

def load_gsam_explained_variance():
    file = data_dir() + '/gsam.explained_variance_ratio.northwest_tropical_pacific.massflux.50pix.nc'
    return xr.open_dataarray(file)

def load_era5_explained_variance():
    file = data_dir() + '/era5.explained_variance_ratio.northwest_tropical_pacific.massflux.2deg.nc'
    return xr.open_dataarray(file)

def load_gsam_era5_levels_explained_variance():
    file = data_dir() + '/gsam_era5_levels.explained_variance_ratio.northwest_tropical_pacific.massflux.50pix.nc'
    return xr.open_dataarray(file) 

def load_gsam_mean_temperature():
    temp_files = 'mean_temperature_profile.gsam.northwest_tropical_pacific.nc'
    temp = xr.open_dataset(f'{project_root_dir()}/data/{temp_files}')
    return temp

def load_era5_mean_temperature():
    temp_files = 'mean_temperature_profile.era5.northwest_tropical_pacific.nc'
    temp = xr.open_dataset(f'{project_root_dir()}/data/{temp_files}')
    return temp

def load_gsam_coarse_50pix(var):
    path = f'/glade/u/home/pangulo/work/gsam_dyamond_winter/northwest_tropical_pacific/{var}_50pix'
    file = path + '/merged.nc'
    ds = xr.open_dataset(file)
    return ds

def load_gsam_coarse_std_50pix(var):
    path = f'/glade/u/home/pangulo/work/gsam_dyamond_winter/northwest_tropical_pacific/{var}_std_50pix'
    file = path + '/merged.nc'
    ds = xr.open_dataset(file)
    return ds

def load_cmorph_precip_2deg():
    path = '/glade/u/home/pangulo/work/cmorph/dyamond_winter/northwest_tropical_pacific/2deg'
    file = path + '/merged.nc'
    ds = xr.open_dataset(file)
    return ds.cmorph

def load_era5_tcwv_2deg():
    path = '/glade/u/home/pangulo/work/era5/dyamond_winter/northwest_tropical_pacific/tcwv'
    file = path + '/coarsened.extracted.northwest_tropical_pacific.e5.oper.an.sfc.128_137_tcwv.ll025sc.2020020100_2020022923.nc'
    ds = xr.open_dataset(file)
    return ds.TCWV

def load_ceres_syn1deg_data():
    path = '/glade/u/home/pangulo/work/ceres/dyamond_winter'
    file = path + '/northwest_tropical_pacific.CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Subset_20200201-20200331.nc'
    ds = xr.open_dataset(file)
    return ds

def load_phase_composite(var, phase):
    path = f"{data_dir()}/moisture_space_composite.{var}.phase{phase}.northwest_tropical_pacific.nc"
    ds = xr.open_dataset(path)
    return ds

def load_composite_circulation(n, p):
    file =  f"{data_dir()}/phase{p}.{n}.circulation.nc"
    return xr.open_dataarray(file)

def load_composite_cloudfraction(n,p):
    file =  f"{data_dir()}/phase{p}.{n}.cloudfrac.nc"
    return xr.open_dataarray(file)

def load_composite_qcpi(n,p):
    file = f"{data_dir()}/phase{p}.{n}.qcpi.nc"
    return xr.open_dataarray(file)

def load_composite_prec(n,p):
    file = f"{data_dir()}/phase{p}.{n}.prec.nc"
    return xr.open_dataarray(file)

def load_composite_prec_se(n,p):
    file = f"{data_dir()}/phase{p}.{n}.prec_se.nc"
    return xr.open_dataarray(file)

def load_composite_min_psi(n,p):
    file = f"{data_dir()}/phase{p}.{n}.min_psi.nc"
    return xr.open_dataarray(file)
## 
def save_figure(fig, filename):
    path = f'{project_root_dir()}/figures/{filename}'
    fig.savefig(path, format='pdf')

def compute_mean_pc_tendency(pcs, method='centered', normed=True):
    if normed:
        pcs /= pcs.std(('lat', 'lon', 'time'))
    match method:
        case 'centered':
            # Centered Difference
            delta_pc = pcs.isel(time=slice(2, None)).data - pcs.isel(time=slice(None, -2)).data   
            # Align time coordinate with data
            delta_pc = pcs.isel(time=slice(1, -1)).copy(data=delta_pc)
            # Hard-coded time step, in hours
            delta_t = 6
        case 'forward': 
            # Forward difference
            delta_pc = pcs.isel(time=slice(1, None)).data - pcs.isel(time=slice(None, -1)).data
            # Align time
            delta_pc = pcs.isel(time=slice(None, -1)).copy(data=delta_pc)
            # Time step
            delta_t = 3
        case 'backward':
            # Backward difference
            delta_pc = pcs.isel(time=slice(1, None)).data - pcs.isel(time=slice(None, -1)).data
            # Align time
            delta_pc = pcs.isel(time=slice(1, None)).copy(data=delta_pc)
            # Time step
            delta_t = 3
        
    return(delta_pc/delta_t)

def bin_stat_by_pcs(pcs, data, pc1_bins, pc2_bins, stat, normed=True):
    if normed:
        pcs /= pcs.std(('lat', 'lon', 'time'))
    x = pcs.sel(mode=1).data.ravel()
    y = pcs.sel(mode=2).data.ravel()
    out = binned_statistic_2d(y, x, data.data.ravel(), stat, bins=[pc2_bins, pc1_bins]).statistic
    return(out)

def compute_theta(pcs, normed=True):
    if normed:
        pcs /= pcs.std(('lat', 'lon', 'time'))
    theta = np.arctan2(pcs.sel(mode=2), pcs.sel(mode=1))
    theta = theta.rename('theta')
    return(theta)

def compute_r(pcs, normed=True):
    if normed:
        pcs /= pcs.std(('lat', 'lon', 'time'))
    r2 = pcs.sel(mode=2)**2 + pcs.sel(mode=1)**2
    return(r2**1/2)
    
def compute_phase_number(theta):
    p = theta.copy(data=np.floor(np.mod((np.array(theta)+(np.pi/8))/(np.pi/4) + 4, 8))+1)
    return(p)

def compute_delta_theta(theta, method='centered'):
    # Use the same method as the pc tendency
    delta = compute_mean_pc_tendency(theta, method, normed=False)
    delta = np.mod(delta + np.pi, 2*np.pi) - np.pi
    return(delta)

def change_in_time(da):
    da_start = da.isel(time=slice(None, -1))
    da_end = da.isel(time=slice(1, None))
    delta = da_start.copy(data=(da_end.data-da_start.data))
    return(delta)

def transition_matrix(initial_phase, final_phase):
    trans_matrix = np.full((9,9), fill_value=np.nan)
    for pi in range(0,9):
        for pf in range(0,9):
            trans_matrix[pi, pf] = ((initial_phase==pi) & (final_phase==pf)).sum()
    row_sums = trans_matrix.sum(axis=1, keepdims=True)
    return trans_matrix/row_sums

def transition_matrix_normalized_anoms(initial_phase, final_phase, data):
    trans_matrix = np.full((9,9), fill_value=np.nan)
    for pi in range(0,9):
        for pf in range(0,9):
            trans_id = np.where((initial_phase==pi) & (final_phase==pf))
            trans_matrix[pi, pf] = np.nanmean(data.data[trans_id])
    row_mean = trans_matrix.mean(axis=1, keepdims=True)
    row_std = trans_matrix.std(axis=1, keepdims=True)
    return (trans_matrix-row_mean)/row_std

def transition_matrix_diff_from_persisting(initial_phase, final_phase, data):
    trans_matrix = np.full((9,9), fill_value=np.nan)
    for pi in range(0,9):
        for pf in range(0,9):
            trans_id = np.where((initial_phase==pi) & (final_phase==pf))
            trans_matrix[pi, pf] = np.nanmean(data.data[trans_id])
    # Compute deviation from the diagonal as a percentage
    for i in range(9):
        diag_value = trans_matrix[i, i]
        if not np.isnan(diag_value) and diag_value != 0:  # Avoid division by zero
            # Calculate the percentage difference from the diagonal value
            trans_matrix[i, :] = ((trans_matrix[i, :] - diag_value) / diag_value) * 100
    
    return trans_matrix