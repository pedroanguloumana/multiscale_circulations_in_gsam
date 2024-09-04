def compute_mean_pc_tendency(pcs, method='centered', normed=True):
    if normed:
        pcs /= pcs.std(('lat', 'lon', 'time'))
    match method:
        case 'centered':
            delta_pc = pcs.isel(time=slice(2, None)).data - pcs.isel(time=slice(None, -2)).data
            delta_pc = pcs.isel(time=slice(1, -1)).copy(data=delta_pc)
            delta_t = 6
        case 'forward': 
            delta_pc = pcs.isel(time=slice(1, None)).data - pcs.isel(time=slice(None, -1)).data
            delta_pc = pcs.isel(time=slice(None, -1)).copy(data=delta_pc)
            delta_t = 3
        case 'backward':
            delta_pc = pcs.isel(time=slice(1, None)).data - pcs.isel(time=slice(None, -1)).data
            delta_pc = pcs.isel(time=slice(1, None)).copy(data=delta_pc)
            delta_t = 3
        
    return(delta_pc/delta_t)

