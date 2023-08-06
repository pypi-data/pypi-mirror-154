# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:32:50 2021

@author: e4hgurge
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from melib.xt import openplot, plotanno, saveplot

DEBUG=False

def skiplines(fp,n, show=False):
    for i in range(0, n):
        line=fp.readline()
        if show: print(line)
    return line

def zonenames(idffile):
    sa=[]
    with open(idffile) as fp:
        while True:
            line=fp.readline()
            if not line: return sa
            if "," in line:
                a=line.split(",")
                if a[0].lstrip()=="Zone":
                    line=fp.readline()
                    a=line.split(",")
                    sa.append(a[0].strip())
                
    

def zonesurfaces(idffile, zonename,epver):
    surfacearray=[]
    if DEBUG: print(idffile, zonename)
    with open(idffile) as fp:
        while True:
            line=fp.readline()
            if not line: return surfacearray
            if "," in line:
                a=line.split(",")
                if a[0].lstrip()=="BuildingSurface:Detailed":
                    if DEBUG: print("045 : ", a[0])
                    line=skiplines(fp, 4)
                    a=line.split(",")
                    if DEBUG: print("    048 : ", a[0])
                    if a[0].lstrip()==zonename:
                        if epver==6:
                            nskip=7
                        else:
                            nskip=6
                        a=skiplines(fp, nskip, show=DEBUG).split(",")
                        n=int(a[0])
                        if DEBUG: print("Number of vertices = %d"%n)
                        surface=np.zeros([n, 3])
                        for i in range(0, n):
                            line=fp.readline()
                            a=line.split(",")
                            for j in range(0, 3):
                                if ";" in a[j]:
                                    s=a[j].split(";")[0]
                                else:
                                    s=a[j]
                                surface[i,j]=float(s.strip())
                        surfacearray.append(surface)
    return surfacearray
            
                        # print(surface)
def plotsurface(ax,surface, lc, name=""):
    a=surface.ravel()
    x=a[0:12:3]
    y=a[1:12:3]
    z=a[2:12:3]
    print("plotsurface")
    print(a)
    ax.plot(np.append(x, x[0]), np.append(y, y[0]), np.append(z, z[0]), lc, label="Wall")
    if name !="":
        ax.legend()
    
def plotzone(idffile, zonename, ax, lc, epver):
    sa=zonesurfaces(idffile, zonename, epver)
    for surface in sa:
        plotsurface(ax, surface, lc)

def idfplot(idffile, filename="", epver=5):
    za=zonenames(idffile)           
    fig=plt.figure()
    ax=fig.add_subplot(projection='3d')
    for z in za:
        plotzone(idffile, z, ax, 'k', epver)
    if filename=="":
        plt.show()
    else:
        fig.savefig(filename)

def jeplot(jcola, startday, nofdays, epo, filename, ylim=[], MD=None, caption="", lc=["k", "b", "r", "g", "m", "c"],
           collabels=""):
    # 10 June 2022 -- collabels is used in epsim.ipynb calls.  I must have lost the collabels
    # version of the jeplot function.  Until I put that back in again, I will ignore it.
    (f1,ax)=openplot(1,0.5)
    hours=np.arange(startday*20, startday*24+nofdays*24)
    i=0
    for j in jcola:
        y=epo.iloc[hours,j]
        plt.plot(hours, y, lc[i])
        ax.plot(hours, y, label="%d %s"%(j,epo.columns[j][0:5]))
        i+=1
    plotanno(ax, xlabel="Hours",  legendloc="upper left")
    if ylim!=[]:
        plotanno(ax, ylim=ylim)
    saveplot(f1, "tmp", filename)
    if MD!=None:
        MD.write(":::30|%s|%s::\n\n"%(filename, caption))
    plt.close()
    
def pltlines(ax, lines, surfaces, lc):
    import numpy as np

    noflines=len(lines)
    i=0
    while i<noflines:
        line=lines[i].rstrip('\n')
        if ":" in line:
            zone=line.split(":")[0]
            if line in surfaces or surfaces==[] or zone in surfaces:
                if zone in surfaces:
                    print(lc, " ZONE MATCH ", zone)
                else:
                    print(lc, "AREA MATCH", line)
                V=np.zeros([4,6])
                for j in range(0,4):
                    i+=1
                    a=lines[i].split(",")
                    for k in range(0,6):
                        V[j,k]=float(a[k])
                    ax.plot([V[j,0],V[j,3]],[V[j,1],V[j,4]],[V[j,2],V[j,5]],lc)
        i+=1
                
    
def pltsln(slnfile, surfaces, highlights, plotfile):
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(projection='3d')
    
    lines=open(slnfile,'r').readlines()
    pltlines(ax, lines, surfaces, 'b')           
    pltlines(ax, lines, highlights, 'r')
    if plotfile=="":
        plt.show()
    else:
        fig.savefig(plotfile)
         
    return lines

            
if __name__ == "__main__":
    import os
    import platform
    if platform.system()=='Darwin':
        EPLUS_DIR_PATH = '/Applications/EnergyPlus-9-5-0'
        local='/Users/Halim/work/eplus/idf'
    else:
        EPLUS_DIR_PATH = u"C:\EnergyPlusV9-5-0"
    idffile="EMSPlantLoopOverrideControl.idf"
    idffile="1ZoneUncontrolled.idf"
    idffile="roofwindowsfloor.idf"
    # examplefile="PythonPluginWindowShadeControl.idf"
    idffile="4ZoneWithShading_Simple_1.idf"
#
    idfpath=os.path.join(local, idffile)
    if not os.path.exists(idfpath):
        print("Not local file.  Try E+ Examples")
        idfpath=os.path.join(EPLUS_DIR_PATH, "ExampleFiles", idffile)   
    DEBUG=True
    za=zonenames(idfpath)           
    fig=plt.figure()
    ax=fig.add_subplot(projection='3d')
    n=len(za)
    lca=["k", "b", "r", "g", "m", "y", "c", "k--", "b--", "r--", "g--"]

    for i in range(0, n):
        plotzone(idfpath, za[i], ax, lca[i%(len(lca))],5)
        print(za[i])
        i+=1
    plt.show()
        
    

#def plotbuildingsurface(fp, ax, surfacename)


# C5_1=np.array([
#       [3.7,11.6,2.4],  # X,Y,Z ==> Vertex 1 {m}
#     [3.7,3.7,2.4],  # X,Y,Z ==> Vertex 2 {m}
#     [26.8,3.7,2.4],  # X,Y,Z ==> Vertex 3 {m}
#     [26.8,11.6,2.4]  # X,Y,Z ==> Vertex 4 {m}
#       ])

# fig=plt.figure()
# ax=fig.add_subplot(projection='3d')
# a=C5_1.ravel()
# x=a[0:12:3]
# y=a[1:12:3]
# z=a[2:12:3]

# ax.plot(np.append(x, x[0]), np.append(y, y[0]), np.append(z, z[0]), label="Wall")
# ax.legend()
# plt.show()

