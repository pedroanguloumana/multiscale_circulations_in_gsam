#!/bin/bash
module load cdo
###################################################
## USER PARAMETERS##
# Region: Equatorial Indian Ocean (Consult README)
## TODO: Add choice of year/month  -PA 8/3/24
##################################################
REGION_NAME="northwest_tropical_pacific"
VAR="tcwv"
LAT_MIN=0
LAT_MAX=20
LON_MIN=130
LON_MAX=170

# Loop through the years and months
for year in 2020; do
    for month in 2; do
        # Format the month to be two digits
        month=$(printf "%02d" $month)
        
        # Directory containing raw ERA5 data for the specific year and month
        input_dir="/glade/campaign/collections/rda/data/ds633.0/e5.oper.an.sfc/${year}${month}"
        # Directory to save output to
        output_dir_base="/glade/work/pangulo/era5/dyamond_winter/${REGION_NAME}/${VAR}"
        # Create the output directory for this year and month if it doesn't exist
        output_dir="$output_dir_base"
        mkdir -p "$output_dir"
        
        echo "Starting processing of NetCDF files for ${year}-${month}..."
        # Loop through each NetCDF file in the input directory
        for file in "$input_dir"/*_${VAR}.*nc; do
            # Extract the filename without the path
            filename=$(basename "$file")
            
            # Print the filename being checked
            echo "Checking file: $filename"

            # Check if the filename contains the variable to extract
            if [[ "$filename" == *"_${VAR}"* ]]; then
                echo "Processing file: $filename"

                # Define the output file path
                output_file="$output_dir/extracted.${REGION_NAME}.${filename%.nc}.nc"
            
                # Extract the latlon box using CDO
                cdo sellonlatbox,$LON_MIN,$LON_MAX,$LAT_MIN,$LAT_MAX "$file" "$output_file"
                
                # Check if the operation was successful
                if [ $? -eq 0 ]; then
                    echo "Successfully extracted latlon box for $filename"
                else
                    echo "Failed to extract latlon box for $filename"
                fi
            else
                echo "Skipping file: $filename"
            fi
        done
        echo "Processing complete for ${year}-${month}."
    done
done

echo "All processing complete."
