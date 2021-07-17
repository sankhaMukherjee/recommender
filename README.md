# recommender

A set of recommender systems that are popularly used for various things.

# 1. Dataset

The data is obtained form a Kaggle competition present here 
[link](https://www.kaggle.com/shivamb/netflix-shows). You will need to download
the data from the file present, and put it in the folder `data/rawData` within 
the same repo. The data folder will not be tracked within this repository. The
data will contain a single CSV file called `netflix_titles.csv`. This CSV file
will contain 12 columns, and each column will be converted into an appropriate
format.

## 1.1. Data Preprocessing

Data is preprocessed in several steps. These are listed below:

1. splitting the columns
2. converting to numeric columns

### 1.1.1. Splitting the Columns

Each column in the dataset is separated into a set of files. The row number of the
original file is put at the beginning of each line to maintain data lineage.

### 1.1.2.Converting to Numeric Columns

Certain categories comprise of a list of categorical values. These are the following:

- cast
- country
- director
- listed_in

Date columns are converted to the difference between a date and a referene date (2021, 12, 31).
These have also been converted to a floating point number between 0 and 1 using simple scaling.
If a date was missing 'December 15, 2017' has been used (arbitrarily chosen).
These are the following:

- release_year
- date_added


# 2. Models



# Requirements

The current version is written with the following configuration:

 - `CudaToolkit 11.0`
 - `cuDNN 8.`
 - `TensorFlow 2.4.1`
 - `torch 1.8.0+cu11`

The code has been tested on a GPU with the following configuration: 

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.119.03   Driver Version: 450.119.03   CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  GeForce RTX 2070    Off  | 00000000:01:00.0  On |                  N/A |
|  0%   47C    P8    21W / 175W |   1456MiB /  7979MiB |      1%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```

For some reason, the current version of tensorflow overflows in memory usage and
errors out for RTX 2070 seres. For that reason, you will need to add the following
lines to your TensorFlow code to prevent that from happening.

```python
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
```

## Authors

Sankha S. Mukherjee - Initial work (2021)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details


