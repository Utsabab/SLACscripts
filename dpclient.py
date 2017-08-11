from psana import *
import psana
import h5py
#import matplotlib.pyplot as plt
import time, os
import itertools
import numpy as np
import scipy.sparse
import scipy.signal
from mpidata import mpidata 

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()	


import sys

def runclient(args):
        experimentName = args.exprun.split(':')[0].split('=')[-1]
        runNumber = args.exprun.split('=')[-1]
        
        sfx = '_' + str(args.tag)
        #srcDir = '/reg/data/ana04/users/zhensu/cxic0415/zhensu/psocake'
        #srcDir = '/reg/d/psdm/cxi/cxic0415/scratch/zhensu/psocake'
        srcDir = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/trial'+runNumber+sfx+'/utsab06/psocake'

    # Read cxi file

	runNum = int(args.exprun.split('run=')[-1])
	runStr = str(runNum).zfill(4)
    	src = srcDir + '/r'+runStr+'/'+experimentName+'_'+runStr+'.cxi'
	f=h5py.File(src,'r')
	posX = f['/entry_1/result_1/peakXPosRaw'].value				#2D array of Position X of all the peaks 
    	posY = f['/entry_1/result_1/peakYPosRaw'].value 			#2D array of Position Y of all the peaks 
    	img = f['/entry_1/data_1/data']
	#print posX, "  ", posX.shape, '\n'
	#print posY, "  ", posY.shape, '\n'
	#print img, "  ", img.shape, '\n'
        #lastEvt = False
	for n, val in enumerate(posX):
                
		if n == args.noe: 
                        #md.endrun()
                        break
                #if n == img.shape[0]-1: lastEvt = True
		if n % (size - 1) != rank - 1: continue
 		md = mpidata()
                px = posX [n, :]						#Array of X co-ordinates of an image
	        py = posY [n, :]						#Array of Y co-ordinates of an image
		img2D = img[n, : :]						#2d Image out of the 3d stack 
		spImg = np.zeros_like(img2D, dtype='int')			#Setting all the pixels in the image to 0
		cordinates = zip(px, py)
		lst_cordinates = list(cordinates)				#zipped list containing tuples of co-ordinate x and y
		for a,b in lst_cordinates:
			#print n, int(b), int(a)
			if int(a) == 0 and int(b) == 0:
                                #print "break once"
				break
			spImg[int(b), int(a)] = 1				#Setting all the corresponding px,py to 1
                #t1=time.time()
		#print "A: ", n, np.sum(spImg)
		win = np.ones((5, 5))
		spImg = scipy.signal.convolve(spImg, win, mode = "same")	#Peaks into 5x5 pixel window 
		
		#print "spImg: ", spImg.dtype
		
    	 	#print "b: ", n, np.sum(spImg)	
		#print "c: ", np.max(spImg)

		if img is None: continue
                #t2 = time.time()
		
		md.addarray('final_image', spImg)
		md.small.index = n
		md.small.runStr = runStr
                #t3 = time.time()
		md.send()
                #t4 = time.time()
                #print "client: ", t4-t3,t3-t2,t2-t1

        md.endrun()

