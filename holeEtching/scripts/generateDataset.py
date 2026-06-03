from holeEtching import holeEtching
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import viennaps as ps
import random


import matplotlib.pyplot as plt

try:
    from .DEFAULTS import DEFAULTS
except ImportError:
    from DEFAULTS import DEFAULTS


data_path = "../../../data/holeEtching/"






def generateDataset(n=2100,fixradius="fixradius",time_list=[0.5,1,1.5],n_workers=None):
    random.seed(42)
    params=[]
    x_list=[]
    y_list=[]


    for _ in range(n):
        ionFlux=DEFAULTS["ionFlux"]*random.uniform(0.5,1.5)
        etchantFlux =DEFAULTS["etchantFlux"]*random.uniform(0.5,1.5)
        oxygenFlux=DEFAULTS["oxygenFlux"]*random.uniform(0.5,1.5)
        meanEnergy=DEFAULTS["meanEnergy"]*random.uniform(0.5,1.5)
        sigmaEnergy=DEFAULTS["sigmaEnergy"]*random.uniform(0.5,1.5)
        if fixradius!="fixradius":
            holeRadius=DEFAULTS["holeRadius"]*random.uniform(0.8,1.2)
            x={"ionFlux":ionFlux,
                "etchantFlux":etchantFlux,
                "oxygenFlux":oxygenFlux,
                "meanEnergy":meanEnergy,
                "sigmaEnergy":sigmaEnergy,
                "holeRadius":holeRadius}
        else:
            x={"ionFlux":ionFlux,
                "etchantFlux":etchantFlux,
                "oxygenFlux":oxygenFlux,
                "meanEnergy":meanEnergy,
                "sigmaEnergy":sigmaEnergy}
            
        y=[]
        for processTime in time_list:
            y_t=holeEtching(**x,processTime=processTime,saveFile=False)
            y.append(y_t)


            # print(y_t)
            # print(len(y_t))

            # pos=[0.03*k for k in range(len(y_t))]
            # high1=[p[0] for p in y_t]
            # high2=[p[1] for p in y_t]
            # plt.figure(figsize=(8, 6))
            # plt.scatter(pos, high1, color='blue', alpha=0.6, s=50)
            # plt.scatter(pos, high2, color='yellow', alpha=0.6, s=50)
            # plt.show()

        x_list.append(x)
        y_list.append(y)
        print(f"{len(y_list)} / {n}")



    np.savez_compressed(data_path+"dataset_"+fixradius+"_%04d"%(n)+".npz", 
                    X_list=np.array(x_list, dtype=object),  
                    Y_list=np.array(y_list, dtype=object),)




if __name__=="__main__":
    generateDataset(fixradius="fixradius")
    generateDataset(fixradius="radius")