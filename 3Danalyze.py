# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 2019

@author: Fan-Jiang + Chi-Kang
"""
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

ATOM_NUMBER = 43272

def ReadEnergyData(filename):
    
    f = open('./%s' %filename, 'r')
    
    edata = []
    for line in f:
        if 'ITEM: ATOMS id c_1 c_2 ' in line: 
            for i, line in enumerate(f):
                edata.append([float(cell) for cell in line.split()])
                if i > ATOM_NUMBER:
                    break
    f.close()
    edata = sorted(edata, key=lambda edata: edata[0])
    return edata

def ReadAtomLocal(filename):
    
    f = open('./%s' %filename, 'r')
    atomlocal=[]
    for line in f:
        if 'Atoms' in line:
            for i, line in enumerate(f):
                atomlocal.append([float(cell) for cell in line.split()])
                if i > ATOM_NUMBER:
                    break
    f.close()

    del atomlocal[0]
    return atomlocal

atomlocal = ReadAtomLocal('R20L300.cylinder')
edata0    = ReadEnergyData('PE_Kb200000_Ka100000_step0')  # initial
edata1    = ReadEnergyData('PE_Kb200000_Ka100000_step330000')  # final

# list to array
atomlocal = np.array(atomlocal)
edata0 = np.array(edata0)
edata1 = np.array(edata1)

#atomlocal = atomlocal[:, 1:] #when u want to see right-now location
atomlocal = atomlocal[:, 3:] # 去掉 ID, 0, 1
# print('shape of atomlocal:', atomlocal.shape)

edata0 = edata0[:ATOM_NUMBER+1, 1:] # 去掉 ID
edata1 = edata1[:ATOM_NUMBER+1, 1:]
# print('shape of edata:', edata.shape)

fig = plt.figure(figsize=(11,9))

#ax = Axes3D(fig) # Method 1
ax = fig.add_subplot(111, projection='3d') # Method 2

# 3D scatter plot
x = atomlocal[:, 0]
y = atomlocal[:, 1]
z = atomlocal[:, 2]
e = [(edata1[:, 0] - edata0[:, 0]) + (edata1[:, 1] - edata0[:, 1])]
#       bending   +  stretching
#e = [(edata1[:, 0] - edata0[:, 0])]  #choose one to analyze

FIG = ax.scatter(x, y, z, e, marker='o', cmap = "hot") #afmhot / Vega20
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# change view side
#for angle in range(0, 360):ax.view_init(30, angle)

fig.colorbar(FIG, shrink=0.8, aspect=20)
plt.show()


# save figure
#fig.savefig('output', transparent=True, dpi=100, pad_inches = 0)
