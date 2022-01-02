import Cluster
import math
import numpy as np
def Dist(V,N):
    res = 0
    for i in range(0,len(V)):
        res +=  (V[i] - N[i])**2 
    res = math.sqrt(res)
    return res

def minDist(Vt,Mt):
    mind = float('inf')
    minC  = None
    for Ni in Mt:
        d = Dist(Vt,Ni.c)
        if d<mind:
            mind = d
            minC = Ni
    return minC

def merge(N1,N2):
    #calc centroid of new cluster
    CW1 = np.array(N1.c) * N1.n
    CW2 = np.array(N2.c) * N2.n
    new_C = (np.add(CW1, CW2))/(N1.n + N2.n)
    new_C = new_C.tolist()

    new_R = max(Dist(new_C,N1.c)+N1.r,Dist(new_C,N2.c)+N2.r)
    new_cluster = Cluster.Cluster(new_C)
    new_cluster.r = new_R
    new_cluster.n =N1.n + N2.n
    
    return new_cluster

def findNeighbors(win,MinPts,Mt):
    if len(Mt) >= MinPts:
        winDistN = []
        #calc distance of every cluster with win cluster
        for Ni in Mt:
            winDistN.append(Dist(win.c,Ni.c))

        # sort base inex
        sortIndex  = sorted(range(len(winDistN)),key=winDistN.__getitem__)

        kDist = winDistN[MinPts - 1]
        win.r = kDist
        winNN = []
        winNN = [Mt[i] for i in sortIndex[0:(MinPts)]]
        return winNN
    else:
        return []

def updateCluster(win,Vt,alpha,winN):
    win.c = np.array(win.c)
    win.c = (win.n * win.c + Vt)/(win.n +1)
    win.n+=1
    width = win.r ** 2
    for Ni in winN:
        influence = math.exp(-(Dist(Ni.c,win.c)/(2*width)))
        diff = win.c - np.array(Ni.c)
        Ni.c = np.array(Ni.c) + alpha * influence * diff
        Ni.c = Ni.c.tolist()

def findoverlap(win,winN):
    overlap = []
    for Ni in winN:
        if win is not Ni:
            if ( Dist(win.c,Ni.c) - (win.r + Ni.r)) < 0:
                overlap.append(Ni)
    return overlap

def mergeCluster(win,overlap):
    merged_Cluster = None
    deleted_Cluster = []
    mergeThreshold = 1
    for Ni in overlap:
         if Dist(Ni.c,win.c)< mergeThreshold:
             if len(deleted_Cluster) ==0:
                 deleted_Cluster.append(win)
                 merged_Cluster = Cluster.Cluster(win.c)
                 merged_Cluster.r = win.r
                 merged_Cluster.n = win.n
             merged_Cluster = merge(Ni,merged_Cluster)
             deleted_Cluster.append(Ni)
    return merged_Cluster,deleted_Cluster
def fadingall(Mt):
    for Ni in Mt:
	fadeThreshold = 10
        if Ni.n < fadeThreshold:
            Mt =  np.delete(Mt,where(Mt==Ni))

