
#PHY 234: Final Project
#Programmer: Zach LaFrankie 

'''
Description: simulate a kinetic aggregation procees 
using the diffusion-limited aggregation model to 
computatinally recreate fractal like growth.

This model is meant to simulate directed bacterial growth 
within a uniform nutrient source via a diffusion limited 
growth (DLG) model. Data from this program will help 
quantify how bacterial growth is effected by the precence
of other nearby colonies.

In this case, 2 horizontally adjacent seeds are set on the 
given lattice. This model highlights the "repelling" nature of nearby 
colonies by calculating the distance between the center of mass of 
each colony after it is fully grown, and its initial seed location.
'''

import numpy as np
import random as r
import matplotlib.pyplot as plt

#note that n must be an odd integer
numSimulations = 1
n = 99
dist = 8

def genFractalData(numParticles=3500, gamma=.93, lambda_=.90, plot=True, printSimData = True, figNum=0):
    
    #define radii
    R_k = (n/2)-1  #killing radius (slightly smaller than lattice)
    R_l = gamma*R_k   #launching radius (fractional size of R_k)
    R_m = lambda_*R_k  #maximum radius (fractional size of R_k)
    
    center_x = n//2
    center_y = n//2
    
    #define radii
    R_k = (n/2)-1  #killing radius (slightly smaller than lattice)
    R_l = gamma*R_k   #launching radius (fractional size of R_k)
    R_m = lambda_*R_k  #maximum radius (fractional size of R_k)
    
    #define colors
    c1 = 'grey'
    c2 = 'blue'

    #create lattice with seeds
    lattice = np.zeros((n,n))
    lattice[n//2 - dist//2, n//2] = 1
    lattice[n//2 + dist//2, n//2] = 2
    
    def particleWalk():
        #generate random point on launching circle
        theta = r.random()*2*np.pi
        x = int(R_l*np.cos(theta))+n//2
        y = int(R_l*np.sin(theta))+n//2
        
        validPosition = True
        continueLoop = True
        latticeAdjacent = False
        
        while validPosition == True and continueLoop==True:
            #move to a random adjacent gridpoint
            rand_distance = r.randint(1,4)
            if rand_distance == 1:
                x+=1
            elif rand_distance == 2:
                x-=1
            elif rand_distance == 3:
                y+=1
            else:
                y-=1
            
            #make sure particle is within killing radius
            distance = np.sqrt((center_x-x)**2+(center_y-y)**2)
            if distance > R_k:
                validPosition = False
                continueLoop = False
                
            elif validPosition == True:
          
                #see if particle is adjacent to another
                a = lattice[x-1, y]
                b = lattice[x+1, y]
                c = lattice[x, y-1]
                d = lattice[x, y+1]
                adjacent_pos = [a,b,c,d]
                if max(adjacent_pos) != 0:
                    latticeAdjacent = True
                
                #if there is an adjacent particle and it is within max radius
                if latticeAdjacent == True and distance < R_m:
                    lattice[x][y] = max(adjacent_pos)
                    continueLoop = False
            
            #plot points to appropriate clusters if adjacent
            if plot == True:
                if validPosition == True and continueLoop == False:
                    if max(adjacent_pos) == 1:
                        plt.figure(figNum)
                        plt.plot(x,y, 'o', color=c1, markersize = 2)
                    elif max(adjacent_pos) == 2:
                        plt.figure(figNum)
                        plt.plot(x,y, 'o', color=c2, markersize = 2)
                        
                    if printSimData == True:
                        print('valid')
    
    #plot clusters
    for i in range(numParticles): 
        particleWalk()
        if printSimData == True:
            print(i)
    plt.axis('equal')
    
    if plot == True:
        #plot seeds
        plt.figure(figNum)
        plt.plot(n//2, n//2, 'Hk', markersize = 6)
        plt.plot(n//2 - dist//2, n//2, 'sr', markersize = 4)
        plt.plot(n//2 + dist//2, n//2, 'sr', markersize = 4)
        plt.axis('equal')    
        
    #plot maximum radius
    for i in range(2000):
        theta = r.random()*2*np.pi
        x = int(R_m*np.cos(theta))+n//2
        y = int(R_m*np.sin(theta))+n//2
        plt.plot(x,y, 'ok', markersize = 2)
    
    #initialize center of mass locations
    avg_col1 = 0
    avg_row1 = 0
    avg_col2 = 0
    avg_row2 = 0
    numParticles1 = 0
    numParticles2 = 0
    
    #extract postions of particles in each cluster to find center of mass
    for row in range(n):
        for col in range(n):
            val = lattice[col,row]
            if val != 0:
                
                #cluster 1
                if val == 1:
                    avg_col1 += col
                    avg_row1 += row
                    numParticles1 += 1
                
                #cluster 2
                else:
                    avg_col2 += col
                    avg_row2 += row
                    numParticles2 += 1
                    
    #calculate center of mass position for each cluster
    avg_col1 = avg_col1 / numParticles1
    avg_row1 = avg_row1 / numParticles1
    avg_col2 = avg_col2 / numParticles2
    avg_row2 = avg_row2 / numParticles2
    
    if plot == True:
        plt.plot(avg_col1, avg_row1, 's', color = 'greenyellow', markersize = 6)
        plt.plot(avg_col2, avg_row2, 's', color = 'greenyellow', markersize = 6)
                    
    return avg_col1, avg_row1, avg_col2, avg_row2, numParticles1, numParticles2



'''
Statistics:
—note that centers of mass and number of partilcles DO count the
 initial seed positions.
'''

#initialize values
avg_col1 = 0
avg_row1 = 0
avg_col2 = 0
avg_row2 = 0
numParticles1 = 0
numParticles2 = 0

#run simulations
for i in range(numSimulations):
    print(f'simulation {i+1}')
    sim = genFractalData(figNum=i, printSimData=False)
    plt.title(f'figure{i+1}')
    avg_col1 += sim[0]
    avg_row1 += sim[1]
    avg_col2 += sim[2]
    avg_row2 += sim[3]
    numParticles1 += sim[4]
    numParticles2 += sim[5]
    
#calculate average COM positions
avg_col1 = avg_col1 / numSimulations
avg_row1 = avg_row1 / numSimulations
avg_col2 = avg_col2 / numSimulations
avg_row2 = avg_row2 / numSimulations
    
seed1_x = n//2 - dist//2 
seed2_x = n//2 + dist//2
seed_y = n//2

#calculate seed COM distances
displacement1_x = avg_col1 - seed1_x
displacement1_y = avg_row1 - seed_y
displacement2_x = avg_col2 - seed2_x
displacement2_y = avg_row2 - seed_y

#output statistics
print()
print(f'Gross center of mass of cluster 1 = ({avg_col1},{avg_row1})')
print(f'Gross center of mass of cluster 2 = ({avg_col2},{avg_row2})')
print(f'Gross displacement of cluster 1 = ({displacement1_x}, {displacement1_y})')
print(f'Gross displacement of cluster 2 = ({displacement2_x}, {displacement2_y})')

print()
print(f'Gross size of cluster 1 = {numParticles1}')
print(f'Gross size of cluster 2 = {numParticles2}')