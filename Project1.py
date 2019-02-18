#!/usr/bin/python3

# for visualization
import matplotlib.pyplot as plt
import numpy as np

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

def get_average_len(frag_lens): # to get the average len of dna fragments
    
    summation = 0

    for i in frag_lens:
        summation+=int(i)

    average = summation/len(frag_lens)

    return average

def print_dist(frag_lens): # for outputting distribution of dna fragments

    # working out solution to visualize fragment distribution

    labels = ['0 - 100', '101 - 200', '201 - 800']
    nums = [0, 0, 0]

    for i in frag_lens:
        if i >= 0 and i <= 100:
            nums[0] += 1
        if i > 100 and i <= 200:
            nums[1] += 1
        if i > 200 and i <= 800:
            nums[2] += 1

    index = np.arange(len(labels))
    plt.bar(index, nums)
    plt.xlabel('ranges', fontsize=5)
    plt.ylabel('fragments', fontsize=5)
    plt.xticks(index, labels, fontsize=5, rotation=30)
    plt.title('Distribution of DNA Fragment Lengths')
    plt.show()


def preprocess(genomeString):
    # Preprocessing of genomeString
    # Additonal proprocessing for flexibility in input types
    for i in range(len(genomeString)):  # for numbered columns
        if genomeString[i].isdigit():
            genomeString = genomeString.replace(genomeString[i], ' ')
    genomeString = genomeString.replace('\n', '')
    genomeString = genomeString.replace('\t', '')
    genomeString = genomeString.replace(' ', '')
    genomeString = genomeString.upper() # if lowercase, make uppercase
    #genomeString = genomeString[int(regionBegin) - 1:]

    return genomeString


# Statistics
frag_lens = [] # This will keep track of each copies fragment length for stats 
noCopies = 0     # This represents the number of times a sequence is NOT copied

# **********************************************
# Beginning of script
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
            if getOS() == 'nt':
                file = os.getcwd() + '/' + file
                genomeString = open(file, 'r').read()
                loop = False
            else:
                file = os.getcwd() + file
                genomeString = open(file, 'r').read()
                loop = False
        except:
            print("Try entering the entire file path. ", end = '')

# preprocessing for genome string:

genomeString = preprocess(genomeString)

#print(genomeString)    # Debugging
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
            print('Valid Range.')
            #for i in range(int(regionBegin) - 1, int(regionLength) + int(regionBegin), 1):
                #print(i)
                #print(genomeString[i], end = '')
            #print('\n')
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
        if ans.lower() == 'y' or ans.lower() == 'yes':
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

# TODO:: Create control statement here



# Create the queues
workQueue = collections.deque([genomeString]) #(2 ** int(cycles))
doneQueue = collections.deque() #(2 ** int(cycles))
workQueue.append(genomeString)
PROCESSES = multiprocessing.cpu_count() - 1
print(str(PROCESSES))
#print(getTaqFallOff())  # Debugging
print(forwardPrimer)
print(backwardPrimer)
#print(workQueue)     # Debugging
print(LCSubStr(forwardPrimer, genomeString))    # Debugging
print(LCSubStr(backwardPrimer, genomeString))   # Debugging

counter = 0
while counter != int(cycles):    # This will run as many times as cycles
    if counter % 2 == 0:         # This tests for which queue to work from
        while len(workQueue) != 0:

            #frag_lens.append(len(workQueue))
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
                frag_lens.append(len(w))
                doneQueue.append(y)
                frag_lens.append(len(y))
            else:
                doneQueue.append(w)
                frag_lens.append(len(w))
                doneQueue.append('')
                noCopies += 1
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
                frag_lens.append(len(x))
                doneQueue.append(z)
                frag_lens.append(len(z))
            else:
                doneQueue.append(x)
                frag_lens.append(len(x))
                doneQueue.append('')
                noCopies += 1
                print('Backward Primer could not bind.')
    if counter % 2 == 1:
        while len(doneQueue) != 0:
            frag_lens.append(len(doneQueue))
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
                frag_lens.append(len(w))
                workQueue.append(y)
                frag_lens.append(len(y))
            else:
                workQueue.append(w)
                frag_lens.append(len(w))
                workQueue.append('')
                noCopies += 1
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
                frag_lens.append(len(x))
                workQueue.append(z)
                frag_lens.append(len(z))
            else:
                workQueue.append(x)
                frag_lens.append(len(x))
                workQueue.append('')
                noCopies += 1
                print('Backward Primer could not bind.')
    counter += 1

#print(workQueue.qsize())    # Just for debugging
#print(workQueue)   # debugging
#print(doneQueue)   # debugging
print('Num of no copies: ' + str(noCopies))
print('Num of copies: ' + str(2 ** int(cycles) * 2 - noCopies))

print('Num of fragments: ' + str(noCopies + (2 ** int(cycles) * 2 - noCopies)))
print('Average fragment len: ' + str(int(get_average_len(frag_lens))))

print_dist(frag_lens)

file = os.getcwd()
if getOS() == 'nt':
    file = file + '\log.txt'
else:
    file = file + '/log.txt'
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

