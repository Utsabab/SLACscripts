"""
The client reads cxi file
Using loop through the number of hits in a run, the events will be broken down to clients alternatively
Each client works to add random uniform noise to the event created using unique sec,nsec and fiducial values
After completion of each events, client sends it to the master 
"""



from psana import *
import psana
import h5py
import matplotlib.pyplot as plt
import time, os
import numpy as np
from mpidata import mpidata 

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#srcDir = '/reg/data/ana04/users/zhensu/cxic0415/zhensu/psocake'
srcDir = '/reg/d/psdm/cxi/cxic0415/scratch/zhensu/psocake'

import sys

def runclient(args):
    # Read cxi file
    #print args.exprun, args.exprun.split('run=')[-1]
    runNum = int(args.exprun.split('run=')[-1])
	
    runStr = str(runNum).zfill(4)
    src = srcDir + '/r'+runStr+'/cxic0415_'+runStr+'.cxi'
    f=h5py.File(src,'r')
    sec = f['/LCLS/machineTime'].value
    nsec = f['/LCLS/machineTimeNanoSeconds'].value
    fiducial = f['/LCLS/fiducial'].value
    print len(sec)
    zipall = zip(sec, nsec, fiducial)
    lst_zipall = list(zipall)
    numImages = len(sec)
    f.close()

    ds = psana.DataSource(args.exprun+':idx')
    run = ds.runs().next()
    det1 = psana.Detector(args.areaDetName)
    md = mpidata()    
    for nevents,val in enumerate(lst_zipall):
	if nevents == args.noe : break
	if nevents % (size-1) != rank - 1: continue	# different ranks look at different events	
	#print rank, nevents

	et = psana.EventTime(int((sec[nevents]<<32)|nsec[nevents]),fiducial[nevents])
	evt = run.event(et)
	#print sec[nevents], nsec[nevents], fiducial[nevents]	
	#print evt
	calib = det1.calib(evt)
	
	absError = 30. # ADU				
    	#Important: unbonded pixels must not be SZ compressed
    	noise = np.random.uniform(low=-absError/2, high=absError/2, size=calib.shape) * det1.mask_comb(evt, mbits=1)
    	noisyCalib = np.round(noise + calib)		# adding uniform random noise of 30 ADU
    	#error = calib - noisyCalib	

	counter = 0
        img = np.zeros((1480,1552))
        for quad in range(4):
            for seg in range(8):
                img[seg * 185:(seg + 1) * 185, quad * 388:(quad + 1) * 388] = noisyCalib[counter, :, :]
                counter += 1
        if nevents % 100 == 0: print "Progress: ", nevents 
	
	if img is None: continue
	
	md.addarray('noisyCalib', img)
	md.small.index = nevents
	md.small.runStr = runStr
	md.send()
	
    md.endrun() 
    

