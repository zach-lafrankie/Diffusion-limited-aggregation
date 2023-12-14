
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
of other nearby colonies.In this case, a single seed is set
in the center of a lattice and the distribution of particles
around the center seed is caluclated.
'''

import numpy as np
import random as r
import matplotlib.pyplot as plt

#note that n must be an odd integer

numSimulations = 5

def genFractalData(n=99, numParticles=900, gamma=.82, lambda_=.78, plot=True, printData = True, figNum=0):
    
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
    c1 = (0.0, 0.0, 1.0)

    #create lattice with seeds
    lattice = np.zeros((n,n))
    lattice[n//2, n//2] = 1
    
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
                
                #if there is an adjacent particle and it is within max radius, plot it
                if latticeAdjacent == True and distance < R_m:
                    lattice[x][y] = max(adjacent_pos)
                    continueLoop = False
                    if plot == True:
                        plt.plot(x,y, 'o', color=c1, markersize = 2)
                        if printData == True:
                            print('valid')
               
    
    #plot clusters
    for i in range(numParticles): 
        particleWalk()
        if printData == True:
            print(i)
    plt.axis('equal')
    
    if plot == True:
        #plot seeds
        plt.plot(n//2, n//2, 'or', markersize = 4)
        plt.axis('equal')
        
        #plot clusters
        for i in range(numParticles): 
            particleWalk()
            if printData == True:
                print(i)
        plt.axis('equal')
            
        #plot maximum radius
        for i in range(2000):
            theta = r.random()*2*np.pi
            x = int(R_m*np.cos(theta))+n//2
            y = int(R_m*np.sin(theta))+n//2
            plt.plot(x,y, 'ok', markersize = 2)
    
    #define seed quadrant counts
    seed1_q1 = 0
    seed1_q2 = 0
    seed1_q3 = 0
    seed1_q4 = 0
    
    #save seed locations
    seed1_x = n//2 
    seed_y = n//2 
    
    #go through lattice
    for row in range(n):
        for col in range(n):
            
            val = lattice[col,row]
            if val != 0:
                
                #check left of seed
                if col < seed1_x:
                    if row > seed_y:         #check above seed_y
                        seed1_q2 += 1
                    elif row < seed_y:       #check below seed_y
                        seed1_q3 += 1 
                    
                #check right of seed 
                elif col > seed1_x: 
                    if row  > seed_y:        #check above seed_y
                        seed1_q1 += 1
                    elif row < seed_y:       #check below seed_y
                        seed1_q4 += 1
                        
                        
    clusterSize1 = 0
    clusterSize2 = 0
    for row in range(n):
        for col in range(n):                #calculate size of each cluster
            if lattice[col,row] != 0:
                if lattice[col,row] == 1:
                    clusterSize1 += 1
                else:
                    clusterSize2 += 1
                    
    #calculate number of (or percentages) of particles in each quadrant 
    P_s1q1 = seed1_q1 #/ (seed1_q1 + seed1_q2 + seed1_q3 + seed1_q4)
    P_s1q2 = seed1_q2 #/ (seed1_q1 + seed1_q2 + seed1_q3 + seed1_q4)
    P_s1q3 = seed1_q3 #/ (seed1_q1 + seed1_q2 + seed1_q3 + seed1_q4)
    P_s1q4 = seed1_q4 #/ (seed1_q1 + seed1_q2 + seed1_q3 + seed1_q4)
            
    if printData == True:
        #number of particles (not including particles along seed axis)
        print()
        print(f'seed_q1 = {seed1_q1}')
        print(f'seed_q2 = {seed1_q2}')
        print(f'seed_q3 = {seed1_q3}')
        print(f'seed_q4 = {seed1_q4}')
        
        #number of particles (not including seeds) in clusters 
        print()
        print(f'QuadSum1 = {seed1_q1 + seed1_q2 + seed1_q3 + seed1_q4}')
        print(f'clusterSize1 = {clusterSize1-1}')
            
    return P_s1q1, P_s1q2, P_s1q3, P_s1q4



#iterate simulation to find average quadrant percentages
P_s1q1 = 0
P_s1q2 = 0
P_s1q3 = 0
P_s1q4 = 0

for i in range(numSimulations):
    sim = genFractalData(figNum=i, printData=False)
    plt.title(f'figure{i+1}')
    P_s1q1 += sim[0]
    P_s1q2 += sim[1]
    P_s1q3 += sim[2]
    P_s1q4 += sim[3]
    plt.show()
    print(f'simulation {i+1}')
    
#plot statistics
plt.figure(i+1)
bins = ['Quadrant 1', 'Quadrant 2', 'Quadrant 3', 'Quadrant 4']
plt.bar(bins, [P_s1q1, P_s1q2, P_s1q3, P_s1q4])
plt.title('Seed')
#print statistics
print()
print(f'Seed 1, Quadrant 1 = {P_s1q1}')
print(f'Seed 1, Quadrant 2 = {P_s1q2}')
print(f'Seed 1, Quadrant 3 = {P_s1q3}')
print(f'Seed 1, Quadrant 4 = {P_s1q4}')

