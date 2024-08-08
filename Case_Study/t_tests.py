import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind


sns.set()

low = []
high = []

all_data = []



for i in range(11):
    data = pd.read_csv(f"./eosinophils_{i + 1}/assigned_clusters-{i + 1}.csv")
    
    # assumes only two labels
    label_of_minimum = data.groupby("ASSIGNED_CLUSTER")["CD16_32"].mean().idxmin()
    label_of_maximum = data.groupby("ASSIGNED_CLUSTER")["CD16_32"].mean().idxmax()
    
    data.loc[data["ASSIGNED_CLUSTER"] == label_of_minimum,  "ASSIGNED_CLUSTER"] = "low_cr16_32"
    data.loc[data["ASSIGNED_CLUSTER"] == label_of_maximum,  "ASSIGNED_CLUSTER"] = "high_cr16_32"

    all_data.append(data)

    low_cr1632 = data.loc[data["ASSIGNED_CLUSTER"] == "low_cr16_32" ,"CD16_32"]
    high_cr1632 = data.loc[data["ASSIGNED_CLUSTER"] != "high_cr16_32" ,"CD16_32"]

    print("Mean low_cr1632:", low_cr1632.mean(), "Mean high_cr1632", high_cr1632.mean())  
    print(ttest_ind(low_cr1632, high_cr1632, axis=0, equal_var=False))
 

data = pd.concat(all_data)
data.to_csv("eosinophils_parts_combined.csv", index=False)

fig, ax = plt.subplots(nrows=1, ncols=3)
fig.suptitle("Box plots of CD16_32, F480, and Ly6C")


# plot box plot of cr1632
g = sns.boxplot(
    data=[
        data.loc[data["ASSIGNED_CLUSTER"] == "low_cr16_32" ,"CD16_32"].values,
        data.loc[data["ASSIGNED_CLUSTER"] == "high_cr16_32" ,"CD16_32"].values
    ],
    ax=ax[0]
)
g.set(xticklabels=["Cluster 1", "Cluster 2"])
g.set(ylabel="CD16_32")



### F480
g = sns.boxplot(
    data=[
        data.loc[data["ASSIGNED_CLUSTER"] == "low_cr16_32" ,"F480"].values,
        data.loc[data["ASSIGNED_CLUSTER"] == "high_cr16_32" ,"F480"].values
    ],
    ax=ax[1]
)
g.set(xticklabels=["Cluster 1", "Cluster 2"])
g.set(ylabel="F480")


g = sns.boxplot(
    data=[
        data.loc[data["ASSIGNED_CLUSTER"] == "low_cr16_32" ,"Ly6C"].values,
        data.loc[data["ASSIGNED_CLUSTER"] == "high_cr16_32" ,"Ly6C"].values
    ],
    ax=ax[2]
)

g.set(xticklabels=["Cluster 1", "Cluster 2"])
g.set(ylabel="Ly6C")

plt.show()