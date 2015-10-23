#Homework: graphic and indexing
# Khoa Hoang - Fall 2015
#################################
import numpy as np
import matplotlib.pyplot as plt
with open('Image.txt') as file:
    array2d=[[int(value1) for value1 in line.split()]for line in file]

OriginalImage=np.reshape(array2d,(-1,16))
print array2d

Temp =[]
for row in array2d:
    for item in row:
        Temp.append(item)
print Temp

print "\n"

pixel= []

pixel.append(Temp[0])
countInd =[]
find = False

print pixel
print "\n"
for var1 in Temp:
    find = False
    
    for i in range(len(pixel)):
        if pixel[i] == var1:
            find = True
            
            break
        
    if find == False:
        pixel.append(var1)
k = 0
for var2 in pixel:
    for var3 in Temp:
        if var2 == var3:
            k += 1
    countInd.append(k)
    k = 0

print pixel
print "\n"
print countInd

#Combining two 1d array to 2d array to keep the counting and to draw a graph
combined=[]
for i in range(len(pixel)):
    combined.append([])
    for j in range(2):
        if j==0:
            combined[i].append(countInd[i])

        else:
            combined[i].append(pixel[i])

#print combined
#combined= combined.sort(key=lambda x:x[0])
#sorted(combined,key=lambda name:name[0])

def getKey(item):
    return item[1]
combined= sorted(combined,key=getKey)
print "After sorting to have a good value for the graph display"
print combined

print '\n'
#Starting drawing a graph of pixel counting
#valCom = [(col[0],col[1],col[2])for col in CompareT]

y = [col[0] for col in combined]
x= [col[1] for col in combined]

plt.plot(x,y, ':rs')
plt.axis([10,30,0,7]) #10,30 are the x stick; 0,7 is y stick
plt.xlabel("Pixel value")
plt.ylabel("Pixel Count")
plt.show()

#Finish