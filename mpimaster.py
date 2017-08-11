"""
receives the event from client side and saves it in cxi
kills clients if the client is done with the job
"""


from shutil import copyfile
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from psmon import publish
import psmon.plots as psplt
import h5py
import numpy as np
from mpidata import mpidata 
import os
	
def runmaster(nClients):
	f = None
	#srcDir = '/reg/data/ana04/users/zhensu/cxic0415/zhensu/psocake'
	srcDir = '/reg/d/psdm/cxi/cxic0415/scratch/zhensu/psocake'
	destDir = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/utsab06/psocake'
	while nClients > 0:
		md = mpidata()
		md.recv()
		if f is None:
			dst = destDir + '/r'+md.small.runStr+'/cxic0415_'+md.small.runStr+'.cxi'#+'-noisy'
			src = srcDir + '/r'+md.small.runStr+'/cxic0415_'+md.small.runStr+'.cxi'
			if not os.path.exists(destDir + '/r'+md.small.runStr):
                            os.mkdir(destDir + '/r'+md.small.runStr)
			if not os.path.exists(dst): copyfile(src, dst)
			f=h5py.File(dst,'a')
			data = f['/entry_1/instrument_1/detector_1/data']
		if md.small.endrun:
			nClients -= 1 
		else:
			data[md.small.index,:,:] = md.noisyCalib
			#plot(md)

	f.close()

def plot(md):
    print 'Master received image with shape',md.noisyCalib.shape,'and index value',md.small.index
	
	











		
