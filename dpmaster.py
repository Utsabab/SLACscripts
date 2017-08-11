from shutil import copyfile
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from psmon import publish
import psmon.plots as psplt	
import h5py
import numpy as np
from scipy.sparse import csr_matrix
from mpidata import mpidata 
import os
import time
	
def runmaster(args, nClients):

        experimentName = args.exprun.split(':')[0].split('=')[-1]
        runNumber = args.exprun.split('=')[-1]
        runNumberZ = runNumber.zfill(4)
	
	f1 = None
	sfx = '_' + str(args.tag)
	srcDir = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/trial'+runNumber+sfx+'/utsab06/psocake'
	destDir = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/hdf5_files'

	while nClients > 0:

                #t1 = time.time()

		md = mpidata()
		md.recv()
 
                #t2 = time.time()

		if f1 is None:

			name_dir = destDir + '/r'+runNumberZ + sfx

			if not os.path.exists(name_dir):
                            os.mkdir(name_dir)

			dst = name_dir +'/' + experimentName + '_'+runNumberZ+'.h5'	#+'-compressed hdf5'
			
			src = srcDir + '/r'+runNumberZ +'/' + experimentName +'_'+runNumberZ+'.cxi'

			#if not os.path.exists(destDir + '/r'+md.small.runStr):
                            #os.mkdir(destDir + '/r'+md.small.runStr)
			#if not os.path.exists(dst): copyfile(src, dst)
			print "Initializing the environment.... "
			f = h5py.File(src, 'r')					
			d = f['/entry_1/instrument_1/detector_1/data']
                        px = f['/entry_1/result_1/peakXPosRaw']
                        py = f['/entry_1/result_1/peakYPosRaw']
			n = f['/LCLS/eventNumber']
                        method=f['/psocake/input']

 			f1 = h5py.File(dst,'a') 
			data = f1.create_dataset('/data', dtype='int', shape=d.shape, chunks=(1, d.shape[1], d.shape[2]), compression='gzip', compression_opts=1)#creating dataset for binary images
			

			dt = h5py.special_dtype(vlen=bytes)		
			dset = f1.create_dataset("/psocake/input",(1,), dtype=dt)						#creating dataset for raw input
			dset[...] = method

			arr_x = f1.create_dataset('/entry_1/result_1/peakXPosRaw',shape=px.shape, dtype='f')			#creating dataset for 2D-array of Position X
			arr_x[...]= px
		
			arr_y = f1.create_dataset('/entry_1/result_1/peakYPosRaw',shape=py.shape, dtype='f')			#creating dataset for 2D-array of Position Y 
			arr_y[...]= py
			
			evno = f1.create_dataset('/LCLS/eventNumber',shape=n.shape, dtype='int')				#creating dataset for number of events 
			evno[...]= n
			
			print "Done..."
                #t3 = time.time()

		if md.small.endrun:
			nClients -= 1 
		else:
                        data[md.small.index,:,:] = md.final_image
                        print "final: ", md.small.index, md.final_image.shape, np.sum(md.final_image)

                #t4 = time.time()

                #print "master: ", t4-t3,t3-t2,t2-t1

        print "Saving to: ", dst			
	f.close()
	f1.close()

def plot(md):
    print 'Master received image with shape',md.final_image.shape,'and index value',md.small.index
	












		
