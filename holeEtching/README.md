# Data Information
## Data Download
Download the advection diffusion boundary value problem data from:
- PKU drive: https://disk.pku.edu.cn/link/AA5615F62AF08948E4B9F6D7764C96735B

- Name of the data file(N \approx N_max):   fixradius.zip    
                                            radius.zip






# Example Command

## Data Preprocessing
Before running the training or other code, it's necessary to preprocess the data. The first time you run the program, execute the following command in the terminal:
`python pcno_holeEtching_test.py "preprocess_data"`

Once the data preprocessing is completed successfully, you can proceed with the subsequent steps and run the training or other related code as described below.

## Training
To run a training example, you can use the following command in the terminal:

`python pcno_holeEtching_test.py  --train_distribution 'fixradius' --n_train 1000 --train_inv_L_scale 'False'`

Replace the values of `--train_distribution`, `--n_train` according to your specific requirements.




# Parameters

| Name             | Type    | Default Value | Choices                              | Description                                                                                                                                                                                                        |
| ----------------- | ------- | ------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--train_distribution`   | `str`   | `mixed`       | `fixradius`, `radius`,`mixed`       | Specifies the distribution of training data           |
| `--n_train`      | `int`   | `1000`        | `500`, `1000`, `1500`                | Number of training samples to use|
| `--n_test`       | `int`   | `600`         |              | Number of testing samples to use|
| `--train_inv_L_scale`   | `str`   | `False`       | `False` | Specifies whether the spatial length scale is trained.|
| `--lr_ratio`     | `float` | `10`          |                                      | Learning rate ratio of main parameters and L parameters when train_inv_L_scale is set to `independently`. |
| `--batch_size`     | `int` | `8`          |                                      | Batch size. |
