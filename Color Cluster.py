
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

In this case, 6 horizontally adjacent seeds are set on the 
given lattice, and the DLG model is used to simulate bacterial
growth. This model highlights the "repelling" nature of nearby 
colonies. Also, specific colonies are color coded.
'''

import numpy as np
import random as r
import matplotlib.pyplot as plt


n = 201 #size of square lattice 
numParticles = 2200
gamma = .70 #proportion R_l / R_k
lambda_ = .68 #proportion R_m / R_k
dist = 15  #distance between seeds

#define radii
R_k = (n/2)-1  #killing radius (slightly smaller than lattice)
R_l = gamma*R_k   #launching radius (fractional size of R_k)
R_m = lambda_*R_k  #maximum radius (fractional size of R_k)

#create lattice with seeds
lattice = np.zeros((n,n))
lattice[n//2 - 3*dist, n//2] = 1
lattice[n//2 - 2*dist, n//2] = 2
lattice[n//2 - dist, n//2] = 3
lattice[n//2 + dist, n//2] = 4
lattice[n//2 + 2*dist, n//2] = 5
lattice[n//2 + 3*dist, n//2] = 6

center_x = n//2
center_y = n//2

#define radii
R_k = (n/2)-1  #killing radius (slightly smaller than lattice)
R_l = gamma*R_k   #launching radius (fractional size of R_k)
R_m = lambda_*R_k  #maximum radius (fractional size of R_k)

#define colors
c1 = (0.0, 0.5, 0.9)
c2 = (0.1, 0.5, 0.8)
c3 = (0.2, 0.4, 0.7)
c4 = (0.3, 0.4, 0.6)
c5 = (0.4, 0.3, 0.5)
c6 = (0.5, 0.3, 0.4)

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
        if validPosition == True and continueLoop == False:
            if max(adjacent_pos) == 1:
                plt.plot(x,y, 'o', color=c1, markersize = 2)
            elif max(adjacent_pos) == 2:
                plt.plot(x,y, 'o', color=c2, markersize = 2)
            elif max(adjacent_pos) == 3:
                 plt.plot(x,y, 'o', color=c3, markersize = 2)
            elif max(adjacent_pos) == 4:
                 plt.plot(x,y, 'o', color=c4, markersize = 2)
            elif max(adjacent_pos) == 5:
                 plt.plot(x,y, 'o', color=c5, markersize = 2)
            elif max(adjacent_pos) == 6:
                 plt.plot(x,y, 'o', color=c6, markersize = 2)
            print('valid')
            
#plot clusters
for i in range(numParticles): 
    particleWalk()
    print(i)
plt.axis('equal')

#plot seeds
plt.plot(n//2, n//2, 'Hr', markersize = 6)
plt.plot(n//2 - 3*dist, n//2, 'sk', markersize = 3)
plt.plot(n//2 - 2*dist, n//2, 'sk', markersize = 3)
plt.plot(n//2 - dist, n//2, 'sk', markersize = 3)
plt.plot(n//2 + dist, n//2, 'sk', markersize = 3)
plt.plot(n//2 + 2*dist, n//2, 'sk', markersize = 3)
plt.plot(n//2 + 3*dist, n//2, 'sk', markersize = 3)
plt.axis('equal')

'''
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
'''
    