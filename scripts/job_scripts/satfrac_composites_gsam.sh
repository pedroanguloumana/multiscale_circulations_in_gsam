#!/bin/bash
#PBS -N gsam_satfrac_composites
#PBS -A UNSB0034 
#PBS -l walltime=1:00:00
#PBS -q casper
#PBS -j oe
#PBS -k eod
#PBS -m be
#PBS -M pangulo@uw.edu
#PBS -l select=1:ncpus=8:mpiprocs=8
module load conda
conda activate dyamond

python /glade/u/home/pangulo/multiscale_circulations_in_gsam/data-workflows/generate_gsam_moisturespace_composites.py