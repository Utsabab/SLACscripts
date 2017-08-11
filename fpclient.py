from psana import *
import numpy as np
from mpidata import mpidata 

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def runclient(args):
    ds = DataSource(args.exprun+':idx')
    run = ds.runs().next()	
    det1 = Detector(args.areaDetName)
    evtNum = 0

    times = run.times()
    #env = ds.env()
    eventTotal = len(times)
    

    max_img = None
    for nevent in xrange(eventTotal):
        if nevent == args.noe : break
        if nevent%(size-1)!=rank-1: continue # different ranks look at different events
	evt = run.event(times[nevent])
        img = det1.image(evt)

	#print "Hello", "  " 

        if img is None: continue
        if max_img is None:
		max_img = img
        else: 
		max_img = np.maximum(img, max_img)		
		
       	#md.small.intensity = intensity
        #if ((nevent)%2 == 0): # send mpi data object to master when desired
    
    print max_img, np.sum(max_img)
    	
    md=mpidata()

    md.addarray('max_img', max_img)      
    
    md.send()
    
    #md.endrun()	
