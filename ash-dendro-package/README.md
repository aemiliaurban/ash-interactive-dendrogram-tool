# ash-dendro package

This package contains two dendrogram utilities
- utility to split dendrogram by selecting a nodes
- utility to parse R hclust format to linkage matrix used by Scipy

# Example Usage

```
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import numpy as np

from ash_dendro.utils import parse_order_df, parse_heights_df, parse_r_hclust, split_dendrogram

# Input data are expected to be in pandas dataframes
# Iris sample data can be used for this purpose

BASE_PATH = "<INSERT YOUR LOCAL PATH>"
heights = pd.read_csv(f"{BASE_PATH}/iris/heights.csv")
order = pd.read_csv(f"{BASE_PATH}/iris/order.csv")
merge = pd.read_csv(f"{BASE_PATH}/iris/merge.csv")

parsed_order = parse_order_df(order)
parsed_heights = parse_heights_df(heights)

# convert from R hclust format to linkage matrix used in Scipy
parsed_merge = parse_r_hclust(
    merge,
    parsed_heights,
    parsed_order
)

plt.figure()
dendrogram(parsed_merge)
plt.show()

nodes_to_split = [3, 8]
clusters_ids_to_assign = [1, 2]

r = split_dendrogram(
    np.array(parsed_merge),
    nodes_to_split,
    clusters_ids_to_assign,
)
print(r)
```