# Data
This portfolio includes the simulation code for etching, 
The hole etching problem data is avaliable from
- PKU drive:https://disk.pku.edu.cn/link/AA5615F62AF08948E4B9F6D7764C96735B
- this are origin data: dataset_fixradius_2100.npz
                        dataset_radius_2100.npz
- data translated into the function in \Omega :     fixradius.zip    
                                                    radius.zip

## Generate Data from Simulation
if you want to generate data from the simulation,do the follow:

to generate data of hole etching,run
`python generateDataset.py`
we will get:    dataset_fixradius_2100.npz,    dataset_radius_2100.npz


then,to translate the data into the function in \Omega,we need preprocess the data
if  using `$N\approx max_i N_i$`,run
    `python preprocess_data_0.py`
else if using `$N>> max_i N_i$`,run
    `python preprocess_data_1.py`
we will get the portfolio: fixradius ,radius