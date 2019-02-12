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

os.system('clear')
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
if len(genomeString) > 250:
    print("""\nWARNING! the fall off rate is set for a range between [150, 250]. 
Please know that per ThermoFisher's DreamTaq specifications, sequences
longer than 7.5 kb should not be used with this simulation. 
***********************************************************************

Please enter a new base value for fall-off-rate.
""")
    newBaseValueFallOff = input('--> ')

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

os.system('clear')

loop = True
while loop:
    print('What region would you like to be copied? Please enter region beginning,\nthen region ending:')
    regionBegin = input('--> ')
    regionEnd = input('--> ')
    if int(regionEnd) - int(regionBegin) < 200:
        #print out region in easy format
        try:
            for i in range(int(regionBegin) - 1, int(regionEnd), 1):
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

os.system('clear')
print('How many cycles? ', end = '')
cycles = input('--> ')

# Summary
os.system('clear')
print('The file you are using is: ', file)
print('The beginning region is:   ', regionBegin, genomeString[int(regionBegin) - 1])
print('The ending region is:      ', regionEnd, genomeString[int(regionEnd)])
print('The number of cycles is:   ', cycles)
print('\nIs this acceptable?')
input('--> ')
# Create control statement here

# Preprocessing of genomeString
genomeString = genomeString.replace('\n', '')
genomeString = genomeString.replace('\t', '')
genomeString = genomeString[int(regionBegin):]

# Create the queues
workQueue = collections.deque([genomeString]) #(2 ** int(cycles))
doneQueue = collections.deque() #(2 ** int(cycles))
#workQueue.append(genomeString)
PROCESSES = multiprocessing.cpu_count() - 1
print(str(PROCESSES))
print(getTaqFallOff())
counter = 0
while counter != int(cycles):    # Just a test to fill queue
    if counter % 2 == 0:
        while len(workQueue) != 0:
            r = getTaqFallOff()
            y = workQueue.popleft()
            z = y[:r]
            doneQueue.append(y)
            doneQueue.append(z)
    if counter % 2 == 1:
        while len(doneQueue) != 0:
            r = getTaqFallOff()
            y = doneQueue.popleft()
            z = y[:r]
            workQueue.append(y)
            workQueue.append(z)
    counter += 1

#print(workQueue.qsize())    # Just for debugging
print(workQueue)
print(doneQueue)

# I'm thinking have a start queue, duplicate the string and place in done queue
# then restart the cycle switching queues
#def oneCycle():
# if even, work queue -> done queue, if odd, done queue -> work queue

