#!/bin/bash
#SBATCH -o PCNO_train.out
#SBATCH --qos=low
#SBATCH -J HoleEtching
#SBATCH -p GPU80G
#SBATCH --nodes=1 
#SBATCH --ntasks=6
#SBATCH --gres=gpu:1
#SBATCH --time=100:00:00


source activate pytorch 



python pcno_holeEtching_test.py  --train_distribution 'fixradius' --n_train 500 --train_inv_L_scale 'False' > log/pcno_holeEtching_fixradius_500.log
python pcno_holeEtching_test.py  --train_distribution 'fixradius' --n_train 1000 --train_inv_L_scale 'False' > log/pcno_holeEtching_fixradius_1000.log
python pcno_holeEtching_test.py  --train_distribution 'fixradius' --n_train 1500 --train_inv_L_scale 'False' > log/pcno_holeEtching_fixradius_1500.log

python pcno_holeEtching_test.py  --train_distribution 'radius' --n_train 500 --train_inv_L_scale 'False' > log/pcno_holeEtching_radius_500.log
python pcno_holeEtching_test.py  --train_distribution 'radius' --n_train 1000 --train_inv_L_scale 'False' > log/pcno_holeEtching_radius_1000.log
python pcno_holeEtching_test.py  --train_distribution 'radius' --n_train 1500 --train_inv_L_scale 'False' > log/pcno_holeEtching_radius_1500.log


python pcno_holeEtching_test.py  --train_distribution 'mixed' --n_train 500 --train_inv_L_scale 'False' > log/pcno_holeEtching_mixed_500.log
python pcno_holeEtching_test.py  --train_distribution 'mixed' --n_train 1000 --train_inv_L_scale 'False' > log/pcno_holeEtching_mixed_1000.log
python pcno_holeEtching_test.py  --train_distribution 'mixed' --n_train 1500 --train_inv_L_scale 'False' > log/pcno_holeEtching_mixed_1500.log


