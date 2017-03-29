# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:34:44 2017

@author: Hugo
"""

import numpy as np
import re
# generate variables
userIDs = []
itemIDs = []


# open the text file
fileInput = open('nr2000.log')


for line in fileInput:
    # check if the line is a recommendation_request
    if "recommendation_"in line:
        #split the line by the symbols , or :
        splitedLine = re.split(',|:',line)
        # find the element "57", ie the user
        indUser = splitedLine.index('"57"')
        new_user = splitedLine[indUser+1]
        if new_user!="0" and new_user!="1":
            userIDs = np.append(userIDs,new_user)
        # find the element "25", ie the item
        indItem = splitedLine.index('"25"')
        new_item = splitedLine[indItem+1]
        if new_item!="0" and new_item!="1":
            itemIDs = np.append(itemIDs,new_item)

      
userIDs = np.unique(userIDs)
itemIDs = np.unique(itemIDs)

nbUsers = len(userIDs)
nbItems = len(itemIDs)

similarity = np.zeros((nbUsers,nbItems))
for line in fileInput:
    # check if the line is a recommendation_request
    if "recommendation_"in line:
        #split the line by the symbols , or :
        splitedLine = re.split(',|:',line)
        # find the element "57", ie the user
        indUser = splitedLine.index('"57"')
        user = splitedLine[indUser+1]
        # find the element "25", ie the item
        indItem = splitedLine.index('"25"')
        item = splitedLine[indItem+1]
        if user!="0" and user!="1" and item!=0 and item!=1:
            row = userIDs.index(user)
            column = itemIDs.index(item)
            similarity[row,column] = 1



# weight matrix initialized with random floats between 0 and 1
w = np.random.rand(nbUsers,nbItems)
epochs = 100 #number of epochs of training
eta = 0.2 #step size

## Computaion
for i in range (0,epochs):
    print(i)
    for u in range (0,nbUsers):
        ## Similarity
        p = similarity[u,:]
        distance = np.zeros(nbUsers)
        for row in range(0,nbUsers):
            distance[row] = np.dot((p - w[row,:]), np.transpose(p - w[row,:]))
        ind_min = np.argmin(distance)

        # the number of neighbours will decrease every epochs
        neighborhood_size = epochs-i
        
        w[ind_min,:] = w[ind_min,:]+eta*(p - w[ind_min,:])
        if (neighborhood_size>0) :
            for neighbour in range (1,neighborhood_size):
                if (ind_min+neighbour>=nbUsers):
                    w[ind_min+neighbour-nbUsers] = w[ind_min+neighbour-nbUsers]+eta*(p - w[ind_min+neighbour-nbUsers])
                else :
                    w[ind_min+neighbour] = w[ind_min+neighbour]+eta*(p - w[ind_min+neighbour])
                if (ind_min-neighbour<0):
                    w[ind_min-neighbour+nbUsers] = w[ind_min-neighbour+nbUsers]+eta*(p - w[ind_min-neighbour+nbUsers])
                else:
                    w[ind_min-neighbour] = w[ind_min-neighbour]+eta*(p - w[ind_min-neighbour])

fileInput.close()


pos = np.zeros(nbUsers)

for u in range (0,nbUsers):
    p = similarity[u,:]
    distance = np.zeros(nbUsers)
    for row in range(0,nbUsers):
        distance[row] = np.dot((p - w[row,:]), np.transpose(p - w[row,:]))
    ind_min = np.argmin(distance)
    pos[u] = ind_min


order = np.argsort(pos)
output = userIDs[order]
fid = open('output.txt','w')
fid.write(output)
fid.close()