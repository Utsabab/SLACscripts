from psana import *
import numpy as np 
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--noe", help="number of minimum bad pixels", type=int)
args = parser.parse_args()
n = args.noe

runnum = 93
ds = DataSource('exp=cxic0415:run=%d:smd'%runnum)
det = Detector('DscCsPad')

un_img = det.mask(runnum,calib=True,status=True,edges=True,central=True,unbond=True,unbondnbrs=True)
#print un_img
print un_img.shape

fs = 185
ss = 388 

'''for i in range(un_img.shape[0]):
    plt.imshow(un_img[i,:,:],vmax=2,vmin=-2)
    plt.title(i)
    plt.show()
exit()'''

def bp(n):
    for i in range(un_img.shape[0]):
        #counter = 0
        for a in range(ss):
	    x = np.where(un_img[i,:,a] == 0)
	    #type(x)
	    #print x
            ind = len(x[0])
	    if ind >= n:
	        un_img[i,:,a]=0
            #counter += 1 
	    #print un_img
        #print counter    
        #print "Euta frame sakkyo"
    mask_img = det.image(runnum, un_img)

    plt.imshow(mask_img, vmin=-2,vmax=2,interpolation='none')
    plt.show()

bp(n)


#y = np.where(un_img[31,175,:] == 0)
#print y

		
