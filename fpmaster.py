from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from psmon import publish
import psmon.plots as psplt
import h5py
import numpy as np
from mpidata import mpidata
import matplotlib.pyplot as plt 

def runmaster(nClients):
    final_img = None
    
    while nClients > 0:
        # Remove client if the run ended
        md = mpidata()
        md.recv()
	#print md.max_img.shape
	if final_img is None:
		final_img = md.max_img
	else:
		#print "Lunch lunch", "  "
		final_img = np.maximum(final_img, md.max_img)
                
	nClients -= 1
        #if md.small.endrun:
            
    
    #print final_img
    #print np.sum(final_img)
    #print 'Master received image with shape',final_img.shape 
    #,'and intensity',md.small.intensity
	
    #plt.imshow(final_img, vmax=300)
    #plt.show()
    np.save("/reg/d/psdm/cxi/cxitut13/res/autosfx/avg_img", final_img)
    




'''def plot(md):
    print final_img
    print 'Master received image with shape',final_img.shape 
    #,'and intensity',md.small.intensity'''
