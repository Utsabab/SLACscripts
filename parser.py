import itertools 
import os 
import re
import numpy as np
import h5py
'''
src = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/utsab06/psocake/r0098/cxic0415_0098.stream'
dst = '/reg/d/psdm/cxi/cxitut13/scratch/utsab06/hdf5_files/r0098_1/cxic0415_0098.h5''''

f = open(src, 'r')
lines = f.readlines() 
f.close()

linenum = []                                                               #array storing line number of the line found
content = []                                                               #array storing content of the line found

for i, line in enumerate(lines):                 	                   #iterates through the txt file
    if re.match('^Event:.+/', line):                                                                           
        linenum.append(i+1)
        content.append(line)
    elif "----- Begin chunk -----" in line:
        linenum.append(i+1)
        content.append(line)
    elif re.match('\s+h.+panel$', line):         
        linenum.append(i+1)
        content.append(line)
    elif "End of reflections" in line:
        linenum.append(i+1)
        content.append(line)

start = []                                          
end = []
linenumevent = []
lst_peaks = []
evno = []

for i,x in enumerate(content):						#appending to array to find start and end of a pattern
    if re.match('\s+h.+panel$', x):
        start.append(linenum[i])
        linenumevent.append(linenum[i-1])				#append the linenumber of every event
    if "End of reflections" in x:
        end.append(linenum[i])
   
#print len(linenumevent)

'''function parses through the line containg event number and splits to return the event number, takes the linenumber of the line containing event number as parameter'''
def getevent(num):							 					
    myeve = lines[num - 1]
    lst_event = []
    lst_event.append(myeve.split()[1][2:])
    return lst_event
 
for i in linenumevent:
    temp=getevent(i)
    evno += temp

'''function takes start and end line number of an indexed pattern and returns two arrays containing indexed x and y co-ordinate'''
def getcoor(x, y):
    myChunk = lines[x:y-1]	
    px = np.empty((y-x)-1,)
    py = np.empty((y-x)-1,) 
    for i, val in enumerate(myChunk):	
        px[i] = myChunk[i].split()[7]
        py[i] = myChunk[i].split()[8]
    return px, py
    #print len(px), len(py)

zipall = zip(start, end)        					#zipping two list of arrays 
lst_zipall = list(zipall) 

for a,b in lst_zipall:          					#loop through the zipped list and using function getcoor to get the coordinates and store in an array lst_peaks
    q = getcoor(a, b)
    lst_peaks += q   

#print evno
#print len(evno)
f1 = h5py.File(dst,'a')

if '/entry_1/result_1/indexedXPeaks' in f1:				#if the list of x coordinates already exist delete
    f1.__delitem__('/entry_1/result_1/indexedXPeaks')	
indPeaksX = f1.create_dataset('/entry_1/result_1/indexedXPeaks',shape=(len(linenumevent),2048),dtype='f') #create dataset for indexed list of x peaks in  h5 file

if '/entry_1/result_1/indexedYPeaks' in f1:                     	#if the list of y coordinates already exist delete
    f1.__delitem__('/entry_1/result_1/indexedYPeaks')	
indPeaksY = f1.create_dataset('/entry_1/result_1/indexedYPeaks',shape=(len(linenumevent),2048),dtype='f') #create dataset for indexed list of y peaks in  h5 file

counter = 0
for i,a in enumerate(lst_peaks):
    a = a[0:2048]							#the size of the cheetah format can hold 2048 elements on x axis 
    if i % 2 == 0:							#if divisible by 2 then it's the list of x coordinates in the zipped list
        indPeaksX[counter,:len(a)]= a 
        counter = counter + 1

counter = 0 
for i,b in enumerate(lst_peaks):
    b = b[0:2048]
    if i % 2 is not 0:							#if not divisible by 2 then it's the list of y coordinates in the zipped list
        indPeaksY[counter,:len(b)]= b
        counter = counter + 1

if '/entry_1/result_1/indexedevno' in f1:				#create dataset for the event numbers in h5 file
    f1.__delitem__('/entry_1/result_1/indexedevno')
indevno = f1.create_dataset('/entry_1/result_1/indexedevno',shape=(len(linenumevent),),dtype ='int')

for i,val in enumerate(evno):						#append event numbers into the database in h5 file 
    indevno[i]= int(val)

print "Saving to: ", dst
print f1['entry_1/result_1/indexedevno'].value 
print f1['entry_1/result_1/indexedXPeaks'].value
print f1['entry_1/result_1/indexedYPeaks'].value  
f1.close()

        #for x in range(len(evno)):
            #print a, len(a)
            #print "####", x, indPeaksX[x,:].shape, indPeaksX[x,:len(a)].shape, a.shape, len(a)
            
