SLACscripts
Scripts written during the course of summer of internship at SLAC

This README file guides you through the process of running all the scripts available in this repository. 

Also the scripts contain comments on it to better understand the steps.


------------------------------------------------------------------------------------------------------------
mpi_driver.py -- runs the master and client script

imaster.py -- Initial master side script for MPI parallel computing\
iclient.py -- Initial client side script for MPI parallel computing

###### running imaster.py and iclient.py\
bsub -q psnehq -n 16 -o /reg/d/psdm/cxi/cxitut13/scratch/utsab06/%J.out \
mpirun python mpi_driver.py exp=cxic0415:run=98 DscCsPad

Remember to import right client and master script before running mpi_driver.py each time
------------------------------------------------------------------------------------------------------------

mpimaster.py -- master side script for noise addition in the image files  
mpiclient.py -- client side script for noise addition in the image files

$running mpimaster.py and mpiclient.py 
======================================
bsub -q psnehq -n 16 -o /reg/d/psdm/cxi/cxitut13/scratch/utsab06/%J.out \
mpirun python mpi_driver.py exp=cxic0415:run=98 DscCsPad

Remember to import right client and master script before running mpi_driver.py each time
------------------------------------------------------------------------------------------------------------

dpmaster.py -- master side script for converting cxi image files into dense image h5 files 
dpclient.py -- client side script for converting cxi image files into dense image h5 files 

$running dpmaster.py and dpclient.py 
====================================
bsub -q psnehq -n 16 -o /reg/d/psdm/cxi/cxitut13/scratch/utsab06/%J.out \
mpirun python mpi_driver.py exp=cxic0415:run=98 DscCsPad -t 1

./runDP runs the script locally 
./runBatchDP runs it in the servers 
------------------------------------------------------------------------------------------------------------

fpmaster.py -- master side script for finding the maxima image in a run
fpclient.py -- client side script for finding the maxima image in a run

$running fpmaster.py and fpclient.py 
====================================
bsub -q psnehq -n 16 -o /reg/d/psdm/cxi/cxitut13/scratch/utsab06/%J.out \
mpirun python mpi_driver.py exp=cxic0415:run=98 DscCsPad

Remember to import right client and master script before running mpi_driver.py each time
------------------------------------------------------------------------------------------------------------

badpixel.py -- script to cover the bad pixels on detector pad to reduce unwanted peaks in an image

$running badpixel.py 
====================
./runbadpixel
------------------------------------------------------------------------------------------------------------

parser.py -- script to parse the indexed stream file to get the predicted x and y coordinates 

Remember to change the source file inside the code itself before running the script 

$running parser.py  
==================
./runparser
------------------------------------------------------------------------------------------------------------

