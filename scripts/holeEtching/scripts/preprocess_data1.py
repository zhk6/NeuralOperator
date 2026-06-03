import numpy as np
import math
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from holeEtching import holeEtching
import viennaps as ps

try:
    from .DEFAULTS import DEFAULTS
except ImportError:
    from DEFAULTS import DEFAULTS

data_path = "../../../data/holeEtching/"

def nearest_integer(num, tolerance=1e-9):
    """
    如果接近整数，返回该整数；否则返回None
    """
    if abs(num - round(num)) <= tolerance:
        return round(num)
    return None


def preprocess_data(filename):
    data=np.load(data_path+"dataset_"+filename+"_2100"+".npz", allow_pickle=True)
    x_list=data["X_list"]
    y_list=data["Y_list"]


    gridDelta=DEFAULTS["gridDelta"]
    holeRadius=DEFAULTS["holeRadius"]
    maskHeight=DEFAULTS["maskHeight"]
    etchStopDepth=DEFAULTS["etchStopDepth"]
    etchStopDepth=-3.40

    nx=51//3+1
    ny=int((maskHeight-etchStopDepth)/gridDelta)

    main_param=["holeRadius","ionFlux","etchantFlux","oxygenFlux","meanEnergy","sigmaEnergy"]

    # 点位，值，粒子


    new_data=[]

    os.makedirs("holeEtching_data", exist_ok=True)

    deep=0

    for i in range(len(x_list)):
        p=[ [i*gridDelta,0,0,0,0,0,0,0,0] for i in range(nx+ny) ]
        # py=[ [i*gridDelta,0,0] for i in range(int(etchStopDepth/gridDelta),ny)]
        # p=px+py

        x=x_list[i]
        y=y_list[i]
        

        
        for k in range(len(y)):
            y_k=y[k]
            
            deep=min(deep,y_k[0][1])
            for j in range(-1,-1-len(p),-1):
                if j+len(y_k)>=0:
                    node=y_k[j]
                    p[j][2*k+1]=node[0]
                    p[j][2*k+2]=node[1]
                else:
                    p[j][2*k+2]=node[1]

        ps.setDimension(DEFAULTS["D"])
        ps.Logger.setLogLevel(eval(f"ps.LogLevel.{DEFAULTS['logLevel']}"))
        ps.Length.setUnit(DEFAULTS["lengthUnit"])
        ps.Time.setUnit(DEFAULTS["timeUnit"])
        geometry = ps.Domain(
        gridDelta=DEFAULTS["gridDelta"],
        xExtent=DEFAULTS["xExtent"],
        yExtent=DEFAULTS["yExtent"],
        )

        holeRadius=x['holeRadius'] if 'holeRadius' in x else DEFAULTS['holeRadius']
        ps.MakeHole(
            domain=geometry,
            holeRadius=holeRadius,
            holeDepth=0.0,
            maskHeight=DEFAULTS["maskHeight"],
            maskTaperAngle=DEFAULTS["taperAngle"],
            holeShape=ps.HoleShape.HALF,
        ).apply()
        mesh = geometry.getSurfaceMesh(addInterfaces=False)
        y0 = mesh.getNodes()
        # print(y0)
        for j in range(-1,-1-len(p),-1):
            if j+len(y0)>=0:
                # print(j)
                # print(len(y0))
                node=y0[j]
                p[j][7]=node[0]
                p[j][8]=node[1]
            else:
                p[j][8]=node[1]



        

        # for node in y:
        #     t=nearest_integer(node[0]/gridDelta)
        #     if t!=None:
        #         p[t][1]=node[1]
        #     else:
        #         t=nearest_integer(node[1]/gridDelta,tolerance=0.1)
        #         if t!=None:
        #             p[t+len(px)+int((0-etchStopDepth)/gridDelta)][1]=node[0]
        #         else:
        #             x+1

        for param in main_param:
            para=x[param] if param in x else DEFAULTS[param]

            if param=="holeRadius":
                continue

                # for j in range(len(p)):
                #     influence_x=(j-ny)-para/gridDelta
                #     if influence_x<0:
                #         p[j][7]=1
                #     else:
                #         p[j][7]=1-influence_x
                #         break
                #     # p[j][7]=1/(1+np.exp(10*gridDelta*influence_x))
                #     # p[j][7]=para
            else:
                for j in range(len(p)):
                    p[j].append(para)
    
        # print(i)

        
        np.save(f"{data_path}/{filename}/data_{i:05d}.npy", p)


    print(f'deep={deep}')
    print(f"{filename}  saved")
    # np.save("process_holeEtching_data.npy",new_data)


if __name__=="__main__":

    preprocess_data("fixradius")
    preprocess_data("radius")


