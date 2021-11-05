# # PS4

'''
Author: Chittaranjan
chitt@umich.edu
'''

# +
# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists
import scipy.stats as st
from collections import defaultdict

from intervals import get_interval_estimate
# -

# ## Q0 - Topics in Pandas

# ### Sparse Data Structures
# - Pandas provides a way of efficiently storing "sparse" data structures
# - A sparse data structure is one in which a majority of the values are
# omitted (to be interpreted as 0, or NaN, or any other value)
# - It can be thought of as a "compressed" representation, as all values are
# not explicitly stored in the data structure

# ### Creating a Sparse Data Frame
# - Sparse data frames can be created using `pd.arrays.SparseArray`
# - Has a dtype of `Sparse` which has two values associated with it,
#     - Type of non-omitted values (Eg: float, int etc)
#     - Value of the elements in the array that aren't actually stored
# (Eg: 0, nan)
#

s = pd.Series(pd.arrays.SparseArray([1] * 2 + [np.nan] * 8))
s

# `Sparse[float64, nan]` indicates that all values apart from `nan` are stored,
#  and they are of type float.

# ### Memory Efficiency
# - The `memory_usage` function can be used to inspect the number of bytes
# being consumed by the Series/DataFrame
# - Comparing memory usage between a SparseArray and a regular python list
# represented as a Series depicts the memory efficiency of SparseArrays

# +
N = 1000  # number of elements to be represented

proportions = list(range(100, N+1, 100))
sparse_mems = []
non_sparse_mems = []
for proportion in proportions:
    sample_list = [14] * proportion + [np.nan] * (N - proportion)
    sparse_arr = pd.Series(
        pd.arrays.SparseArray(sample_list)
    )
    sparse_mem = sparse_arr.memory_usage()
    sparse_mems.append(sparse_mem)

    non_sparse_arr = pd.Series(sample_list)
    non_sparse_mem = non_sparse_arr.memory_usage()
    non_sparse_mems.append(non_sparse_mem)

x = list(map(lambda p: p / N, proportions))
_ = plt.plot(x, non_sparse_mems)
_ = plt.plot(x, sparse_mems)
_ = plt.ylabel("Memory Usage (bytes)")
_ = plt.xlabel("Proportion of values")
_ = plt.legend(["Non-Sparse", "Sparse"])
_ = plt.title("Comparison of Memory Usage (Size=1000)")
# -

# ### Memory Efficiency (Continued)
# - The Sparse Arrays consume much less memory when the density is low
# (sparse-ness is high)
# - As the density increases to where 50-60% of the values are not nan
# (i.e ommittable), memory efficiency is worse
