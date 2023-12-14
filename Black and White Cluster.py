
#PHY 234: Final Project
#Programmer: Zach LaFrankie 

'''
Description: simulate a kinetic aggregation procees 
using the diffusion-limited aggregation model to 
computatinally recreate fractal like growth.

This model is meant to simulate directed bacterial growth 
within a uniform nutrient source via a diffusion limited 
growth (DLG) model. 
'''

#%matplotlib qt

import numpy as np
import random as r
import matplotlib.pyplot as plt

n = 235 #size of square lattice 
numParticles = 21000
gamma = .89 #proportion R_l / R_k
lambda_ = .86 #proportion R_m / R_k
dist = 30  #distance between seeds

#create lattice with seed(s)
lattice = np.zeros((n,n))
#lattice[n//2 - dist//2, n//2] = 1
lattice[n//2, n//2] = 1
#lattice[n//2 + dist//2, n//2] = 1

center_x = n//2
center_y = n//2

#define radii
R_k = (n/2)-1  #killing radius (slightly smaller than lattice)
R_l = gamma*R_k   #launching radius (fractional size of R_k)
R_m = lambda_*R_k  #maximum radius (fractional size of R_k)

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
            
        if validPosition == True:
      
            #see if particle is adjacent to another
            if lattice[x-1][y] == 1 or lattice[x+1][y] == 1:
                latticeAdjacent = True
            
            elif lattice[x][y-1] == 1 or lattice[x][y+1] == 1:
                latticeAdjacent = True
            
            #if there is an adjacent particle and it is within max radius
            if latticeAdjacent == True and distance < R_m:
                lattice[x][y] = 1
                continueLoop = False
                plt.plot(x,y, 'ok', markersize = 2)
                print('valid')
            
#plot clusters
for i in range(numParticles): 
    particleWalk()
    print(i)
plt.axis('equal')

#plot seeds
#plt.plot(n//2 - dist//2, n//2, 'or', markersize = 4)
plt.plot(n//2, n//2, 'or', markersize = 4)
#plt.plot(n//2 + dist//2, n//2, 'or', markersize = 4)


#plot maximum radius
for i in range(2000):
    theta = r.random()*2*np.pi
    x = int(R_m*np.cos(theta))+n//2
    y = int(R_m*np.sin(theta))+n//2
    plt.plot(x,y, 'or', markersize = 2)
  
#plot launching radius
for i in range(2000):
    theta = r.random()*2*np.pi
    x = int(R_l*np.cos(theta))+n//2
    y = int(R_l*np.sin(theta))+n//2
    plt.plot(x,y, 'og', markersize = 2)
    
#plot killing radius
for i in range(2000):
    theta = r.random()*2*np.pi
    x = int(R_k*np.cos(theta))+n//2
    y = int(R_k*np.sin(theta))+n//2
    plt.plot(x,y, 'ok', markersize = 2)
