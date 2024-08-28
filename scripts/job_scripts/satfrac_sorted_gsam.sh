#!/bin/bash
#PBS -N gsam_satfrac_2D
#PBS -A UNSB0034 
#PBS -l walltime=5:00:00
#PBS -q casper
#PBS -j oe
#PBS -k eod
#PBS -m be
#PBS -M pangulo@uw.edu
#PBS -l select=1:ncpus=2:mpiprocs=4
module load conda
conda activate dyamond

python /glade/u/home/pangulo/multiscale_circulations_in_gsam/data-workflows/generate_gsam_satfrac_sorted.py -region 'tropical_nw_pacific' -var '2D' -gridsize 50