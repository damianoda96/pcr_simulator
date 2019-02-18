#!/usr/bin/python3

import multiprocessing
import collections
import time
import os
import random

# default value for taq fall off is 200
def getTaqFallOff(f=200):
	FIXED_FALL_OFF_CONSTANT = f
	randomFallOff = random.randint(-50,50)
	return FIXED_FALL_OFF_CONSTANT + randomFallOff

def getOS():
    if os.name == 'nt':
        return 'cls'
    else:
        return 'clear'

def LCSubStr(X, Y): 
    m = len(X)
    n = len(Y)
    # Create a table to store lengths of 
    # longest common suffixes of substrings.  
    # Note that LCSuff[i][j] contains the  
    # length of longest common suffix of  
    # X[0...i-1] and Y[0...j-1]. The first 
    # row and first column entries have no 
    # logical meaning, they are used only 
    # for simplicity of the program. 
      
    # LCSuff is the table with zero  
    # value initially in each cell 
    LCSuff = [[0 for k in range(n+1)] for l in range(m+1)] 
      
    # To store the length of  
    # longest common substring 
    result = 0 
  
    # Following steps to build 
    # LCSuff[m+1][n+1] in bottom up fashion 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if (i == 0 or j == 0): 
                LCSuff[i][j] = 0
            elif (X[i-1] == Y[j-1]): 
                LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                result = max(result, LCSuff[i][j]) 
            else: 
                LCSuff[i][j] = 0
    return result

clear = getOS()
os.system(clear)
print(os.getcwd())
print('Please enter the file path: ', end = '')
loop = True
while loop:
    file = input('--> ')
    try:
        genomeString = open(file, 'r').read()
        loop = False
    except:
        try:
            file = os.getcwd() + '/' + file
            genomeString = open(file, 'r').read()
            loop = False
        except:
            print("Try entering the entire file path. ", end = '')

print(genomeString)
print("The length of your genome is:", len(genomeString))
# assignment assumes 200 is default value for amplification, option to adjust
# could be added.
#if len(genomeString) > 250:
#    print("""\nWARNING! the fall off rate is set for a range between [150, 250]. 
#Please know that per ThermoFisher's DreamTaq specifications, sequences
#longer than 7.5 kb should not be used with this simulation. 
#***********************************************************************
#
#Please enter a new base value for fall-off-rate The default is 200.
#""")
#    newBaseValueFallOff = input('--> ')

# new logic should be added to adjust fall off rate

loop = True
while loop:
    yesNo = input('Is this correct? --> ')
    if yesNo == 'y' or yesNo == "yes" or yesNo == 'Y' or yesNo == "YES":
        loop = False
    elif yesNo == 'n' or yesNo == "no" or yesNo == 'N' or yesNo == "NO":
        loop = False
    else:
        print("Please try \"y\" or \"n\"")

os.system(clear)

loop = True
while loop:
    print('What region would you like to be copied? The first 20 bases will automatically'
    + ' be set for the primers. Please enter region beginning.')
    regionBegin = input('--> ')
    print('How many bases would you like amplified? The default is 200.')
    regionLength = input('--> ')
    if int(regionLength) < 200:
        #print out region in easy format
        try:
            for i in range(int(regionBegin) - 1, int(regionLength) + int(regionBegin), 1):
                #print(i)
                print(genomeString[i], end = '')
            print('\n')
        except:
            print('Invalid Range. The regions provided are outside of genome.')
        
        print('Does this look correct? ', end = '')
        
        yesNo = input('--> ')
        if yesNo == 'y' or yesNo == "yes" or yesNo == 'Y' or yesNo == "YES":
            loop = False
        elif yesNo == 'n' or yesNo == "no" or yesNo == 'N' or yesNo == "NO":
            print('Try again.')
        else:
            print("Please try \"y\" or \"n\"")
        
    else:
        print('Are you sure? ')
        ans = input('--> ')
        if ans == 'y':
            loop = False
            

if len(genomeString) < 21:
    forwardPrimer = genomeString[:len(genomeString)]
    backwardPrimer = genomeString[:len(genomeString)]
else:
    forwardPrimer = genomeString[(int(regionBegin) - 1):(int(regionBegin) + 19)]
    backwardPrimer = genomeString[int(regionBegin) + int(regionLength) - 19:int(regionBegin) + int(regionLength) + 1]

os.system(clear)
print('How many cycles? ', end = '')
cycles = input('--> ')

# Summary
#os.system(clear)
print('The file you are using is: ', file)
print('The beginning region is:   ', regionBegin, genomeString[int(regionBegin) - 1])
print('The region length is:      ', regionLength, genomeString[int(regionBegin) + int(regionLength)])
print('The number of cycles is:   ', cycles)
print('\nIs this acceptable?')
input('--> ')
# Create control statement here

# Preprocessing of genomeString
genomeString = genomeString.replace('\n', '')
genomeString = genomeString.replace('\t', '')
#genomeString = genomeString[int(regionBegin) - 1:]

# Create the queues
workQueue = collections.deque([genomeString]) #(2 ** int(cycles))
doneQueue = collections.deque() #(2 ** int(cycles))
workQueue.append(genomeString)
PROCESSES = multiprocessing.cpu_count() - 1
print(str(PROCESSES))
#print(getTaqFallOff())
print(forwardPrimer)
print(backwardPrimer)
#print(workQueue)     # Debugging
print(LCSubStr(forwardPrimer, genomeString))
print(LCSubStr(backwardPrimer, genomeString))

counter = 0
while counter != int(cycles):    # This will run as many times as cycles
    if counter % 2 == 0:         # This tests for which queue to work from
        while len(workQueue) != 0:
            w = workQueue.popleft()
            lw = LCSubStr(forwardPrimer, w)
            x = workQueue.popleft()
            lx = LCSubStr(backwardPrimer, x)
            if lw >= 10:
                pos = w.find(forwardPrimer[len(forwardPrimer) - lw:])
                print('Forward Primer pos: ' + str(pos))
                r = getTaqFallOff()
                print('taq: ' + str(r))
                if pos + r > len(w):
                    y = w[pos:]
                else:
                    y = w[pos:r + pos]
                doneQueue.append(w)
                doneQueue.append(y)
            else:
                doneQueue.append(w)
                print('Forward Primer could not bind.')
            if lx >= 10:
                pos = x.find(backwardPrimer)
                pos = pos + lx
                print('Backward Primer pos: ' + str(pos))
                r = getTaqFallOff()
                print('taq: ' + str(r))
                if pos - r < 0:
                    z = x[:pos]
                else:
                    z = x[pos - r:pos]
                doneQueue.append(x)
                doneQueue.append(z)
            else:
                doneQueue.append(x)
                print('Backward Primer could not bind.')
    if counter % 2 == 1:
        while len(doneQueue) != 0:
            w = doneQueue.popleft()
            lw = LCSubStr(forwardPrimer, w)
            x = doneQueue.popleft()
            lx = LCSubStr(backwardPrimer, x)
            if lw >= 10:
                pos = w.find(forwardPrimer[len(forwardPrimer) - lw:])
                print('Forward Primer pos: ' + str(pos))
                r = getTaqFallOff()
                print('taq: ' + str(r))
                if pos + r > len(w):
                    y = w[pos:]
                else:
                    y = w[pos:r + pos]
                workQueue.append(w)
                workQueue.append(y)
            else:
                workQueue.append(w)
                print('Forward Primer could not bind.')
            if lx >= 10:
                pos = x.find(backwardPrimer)
                pos = pos + lx
                print('Backward Primer pos: ' + str(pos))
                r = getTaqFallOff()
                print('taq: ' + str(r))
                if pos - r < 0:
                    z = x[:pos]
                else:
                    z = x[pos - r:pos]
                workQueue.append(x)
                workQueue.append(z)
            else:
                workQueue.append(x)
                print('Backward Primer could not bind.')
    counter += 1

#print(workQueue.qsize())    # Just for debugging
#print(workQueue)   # debugging
#print(doneQueue)   # debugging

file = os.getcwd()
file = file + '\log.txt'
file2 = file + 't'
print(file)
f = open(file, 'w')
f2 = open(file2, 'w')
for i in workQueue:
    f.write(str(i))
    f.write('\n\n')
for i in doneQueue:
    f2.write(str(i))
    f2.write('\n\n')
f.close()
f2.close()

#def oneCycle():
# if even, work queue -> done queue, if odd, done queue -> work queue

