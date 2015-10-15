"""
PROGRAMMING ASSIGNMENT - Lossless Technique
Multimedia System 6010 - Fall2015
Khoa Hoang
"""

import numpy as np
import matplotlib.pyplot as plt
import math
#Creating Huffman Table for Difference
HuffmanEncoder = {0:'1',1:'00',-1:'011',2:'0100',-2:'01011',
                  3:'010100', -3:'0101011',4:'01010100',
                  -4:'010101011',5:'0101010100', -5:'01010101011',
                  6:'010101010100', -6:'0101010101011'}

HuffmanDecoder = {'1':'0', '00':'1', '011':'-1', '0100':'2', '01011':'-2', '010100':'3', '0101011':'-3', '01010100':'4',
                  '010101011':'-4', '0101010100':'5', '01010101011':'-5', '010101010100':'6', '0101010101011':'-6'}

#Test opening the Image pixels values
FileImage = 'TestImage1.txt'
try:
    f=open(FileImage)
    dataImage = f.read()
    f.close()
except IOError:
    print ("Cannot find file: " + FileImage)
    exit()


#Initialize the size of the image
rows = 16
cols = 16

print "\nReading and printing the value (pixels) of the oringinal image:\n"

"""
Read the value of the image into an array (1d) and then convert to 2d array to display
"""
with open('TestImage1.txt') as file:
    array2d=[[int(value1) for value1 in line.split()]for line in file]

OriginalImage=np.reshape(array2d,(-1,16))
print OriginalImage
print "\n"

#Starting a function for each cases of DX
"""
Starting the function
Dx is a string variable that indicates which case (7 predictors)is used
ax, bx, and cx are variables for compressing calculation
ay, by, and cy are variables for decompressing calculation
"""
def Predictor(Dx,ax,bx,cx,ay,by,cy):
    #Initialize the Compression ratio and Bits/pixel of the image for the calculation
    Cr = 0.0
    Bpix = 0.0
    RMSE = 0.0
    TempArray = [] #array to store temporary value
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                TempArray.append(array2d[0][0])
            elif i == 0 and j != 0:
                TempArray.append(array2d[0][j] - array2d[0][j-1])
            elif j == 0 and i != 0:
                TempArray.append(array2d[i][0]-array2d[i-1][0])
            else:
                TempArray.append(int(round(array2d[i][j]-(ax*array2d[i][j-1] + bx*array2d[i-1][j] +cx*array2d[i-1][j-1]))))
            #print TempArray
    print "The coefficients after the prediction in " + Dx + "\n"
    Coeff = np.reshape(TempArray,(-1,16)) #Convert an array 1d to 2d
    print Coeff
    print "\n"
    ###################
    #Begin to convert to binary form after Huffman table
    ###################
    Temp2 =[]
    for n in range(rows*cols):
        if n == 0:
            Temp2.append(bin(TempArray[0])[2:].zfill(8))
        else:
            Temp2.append(HuffmanEncoder[TempArray[n]])
    print "This is compressed image in the form of binary (after Huffman table) in " + Dx +"\n"
    #convert array Temp2 into 2d array and print it
    After = np.reshape(Temp2,(-1,16))
    for col in After:
        print ("{0:12}{1:12}{2:12}{3:12}{4:12}{5:12}{6:12}{7:12}{8:12}{9:12}{10:12}{11:12}{12:12}{13:12}{14:12}{15:12}".format(col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7],col[8],col[9],col[10],col[11],col[12],col[13],col[14],col[15]))
    print "\n"

    ####################
    #Begin to calculate number of bits after Huffman table
    #   and calculate the Compression ratio Cr; the Bits/pixel for the compressed image Bpix
    ####################

    bitnumb = 0
    for item in Temp2:
        bitnumb = bitnumb + len(item)
    print "The number of bits of the compressed image (in " + Dx +"): " + str(bitnumb) + "\n"

    Cr= round((16*16*8./bitnumb),2)
    print "Compression ratio (in " + Dx +"): " + str(round((16*16*8./bitnumb),2)) +'\n'
    Bpix = round((8/Cr),2)

    print "Bits/pixel for the compressed image (in " + Dx +"): " + str(Bpix) + "\n"

    ######################
    #Begin to decompress the image (after Huffman decoder)
    ######################
    Temp22= []
    for k2 in range(len(Temp2)):
        if k2 == 0:
            Temp22.append(int(Temp2[k2],2))
        else:
            Temp22.append(HuffmanDecoder[Temp2[k2]])

    #Convert character into integer to display:
    Temp22 =[int(i) for i in Temp22]
    B22=np.reshape(Temp22,(-1,16))
    print "The image after Huffman decoder: \n"
    print B22
    print "\n"

    ######################
    #Begin to calculate and display the image after decompression
    ######################
    Image_decom = []

    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                Image_decom.append(B22[0][0])
            elif i == 0 and j != 0:
                Image_decom.append(B22[0][j] + Image_decom[j-1])
            elif j == 0 and i != 0:
                Image_decom.append(B22[i][0]+ Image_decom[len(Image_decom)-cols])
            else:
                Image_decom.append(int(round((B22[i][j] + ay*(Image_decom[len(Image_decom)-1]) + by*(Image_decom[len(Image_decom)-cols]) + cy*(Image_decom[len(Image_decom)-cols -1])))))

    #print Image_decom
    print "The image ater decompression \n"
    Decomp = np.reshape(Image_decom,(-1,16))
    print Decomp
    print "\n"


    ######################
    #Begin to calculate the RMS Error
    ######################
    MSE = 0
    for i in range(rows):
        for j in range(cols):
            MSE = MSE + round((1./(rows*cols))*(OriginalImage[i][j]-Decomp[i][j])**2,2)
    RMSE = round(math.sqrt(MSE),2)
    print "The RMS Error in "+ Dx + " is " + str(RMSE) +"\n\n"

    print "**********************************************************"
    print "**********************************************************"
    #Return the Compression ratio and Bits/pixel every cases
    return Cr, Bpix, RMSE
"""
##########################################################
Finish the function and starting to call the main program:
##########################################################
"""

#Initialize a table to compare the compression ratio, the bits/pixel and the RMS Error of 7 cases:

CompareT = [['Object', 'Cr','Bpix','RMSE'],
            ['X^ = A',0,0,0],
            ['X^ = B',0,0,0],
            ['X^ = C',0,0,0],
            ['X^ = A+B-C',0,0,0],
            ['X^ = A+(B-C)/2',0,0,0],
            ['X^ = B+(A-C)/2',0,0,0],
            ['X^ = (A+B)/2',0,0,0]]


print "*******  In the case of X^ = A ***********"
"""
Case 1: X^ = A or X^= 1*A + 0*B + 0*C ==> so ax = 1, bx = 0, cx = 0
Similar for ay=1, by = 0, cy = 0
Then pass these value into the argument of the function
The function return the compression ratio, the Bit/pixel and the RMSE value
Then store those values into the array CompareT in order to compare
"""
CompareT[1][1], CompareT[1][2], CompareT[1][3] = Predictor('the case of X^ = A', 1, 0, 0, 1, 0, 0)

print "\n"

#################################################
#Similar to the case X^=A
print "*******  In the case of X^ = B ***********"
CompareT[2][1], CompareT[2][2], CompareT[2][3] = Predictor('the case of X^ = B', 0, 1, 0, 0, 1, 0)

print "\n"

#################################################
print "*******  In the case of X^ = C ***********"
CompareT[3][1], CompareT[3][2], CompareT[3][3] = Predictor('the case of X^ = C', 0, 0, 1, 0, 0, 1)

print "\n"

#################################################
print "*******  In the case of X^ = A+B-C ***********"
CompareT[4][1], CompareT[4][2], CompareT[4][3] = Predictor('the case of X^ = A+B-C', 1, 1, -1, 1, 1, -1)

print "\n"

####################################################
print "*******  In the case of X^ = A+(B-C)/2 ***********"
CompareT[5][1], CompareT[5][2], CompareT[5][3] = Predictor('the case of X^ = A+(B-C)/2', 1, 0.5, -0.5, 1, 0.5, -0.5)

print "\n"

############################################################
print "*******  In the case of X^ = B+(A-C)/2 ***********"
CompareT[6][1], CompareT[6][2], CompareT[6][3] = Predictor('the case of X^ = B+(A-C)/2', 0.5, 1, -0.5, 0.5, 1, -0.5)

print "\n"
################################################################
print "*******  In the case of X^ = (A+B)/2 ***********"
CompareT[7][1], CompareT[7][2], CompareT[7][3] = Predictor('the case of X^ = (A+B)/2', 0.5, 0.5, 0, 0.5, 0.5, 0)

print "\n"
#################################################################
print"*********************###############***************************"
print "The table value of compression ratio, Bits/pixel and RMSE of 7 cases: \n"
print "\n"

for col in CompareT:
    print ("{0:<18}{1:<10}{2:<10}{3:<10}".format(col[0],col[1],col[2],col[3]))
#print('\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in CompareT]))
print "\n"

valCom = [(col[0],col[1],col[2])for col in CompareT]

"""
Configure values to draw graph: one is for compression ratio, and the other is for Bits/pixel

"""
#Remove the top row in the comparing value table
valCom=np.delete(valCom,(0),axis=0)

#Create empty tables
LabelN = []     #table to store names of 7 cases
CmRa =[]        #table to store value of Compression Ratio
BiPe = []       #table to store value Bits/pixel
for row in valCom:
    LabelN.append(row[0])
    CmRa.append(row[1])
    BiPe.append(row[2])

print "\n"
#Convert the value of Compression ratio from charater to float to draw that graph
CmRa=[float(i) for i in CmRa]
ind1 = np.arange(len(LabelN)) #index of the name of 7 cases
plt.bar(ind1,CmRa)
plt.xticks(ind1+0.3,LabelN)
plt.ylabel('Compression Ratio')
plt.title('Lossless Compression Ratio')
plt.show()

#Draw the graph for Bits/pexil

BiPe=[float(i) for i in BiPe]
plt.bar(ind1,BiPe)
plt.xticks(ind1+0.3,LabelN)
plt.ylabel('Bits/pixel')
plt.title('Lossless Compression (Bits/pixel)')

plt.show()

#Finish