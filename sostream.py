from csv import reader
import Cluster
with open("Dataset_1.csv",'r') as read_obj:
    DS = reader(read_obj)
    M = [[]]
    MinPts = 5
    alpha = 0.1
    numberdelete=[0]
    for Vt in DS:
        numberdelete.append(0)
        Mt = M[-1].copy()
        Vt = list(map(float,Vt))
        win = minDist(Vt,Mt)
        if len(Mt) >= MinPts:

            winN = findNeighbors(win,MinPts,Mt)
            if Dist(Vt,win.c)<=win.r:
                updateCluster(win,Vt,alpha,winN)
            else:
               Mt.append(Cluster.Cluster(Vt))
            overlap = findoverlap(win,winN)
            if len(overlap) > 0 :
               merge_Cluster,deleteClusters =  mergeCluster(win,overlap)
               numberdelete[-1]= len(deleteClusters)
               for dc in deleteClusters:
                   Mt.remove(dc)
               if merge_Cluster is not None:
                   Mt.append(merge_Cluster)
        else:
            Mt.append(Cluster.Cluster(Vt))
        M.append(Mt)