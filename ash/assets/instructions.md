# Instructions
## Introduction to Ash
Ash is an interactive tool for clustering unstructured data. It targets flow cytometry data, but the tool itself is data agnostic.

In flow cytometry, the leading method to cluster data is called manual gating. But manual gating relies on researchers to manually draw boundaries around clusters of cells. This is a time-consuming and subjective process.
Ash aims to facilitate the process by providing tools and visualization to do so.

Recently, there has been progress in GPU accelerated clustering algorithms and Ash serves as a front end to these.
User is expected to provide a raw data (linkage matrix - result of clustering) and assign clusters to different subgroups in Ash.
Ash itself is not a tool for performing clustering, but rather a tool for distinguishing cellular populations and visualizing them.  

## Key features of Ash
### Ease of access
Working with clustered data often requires programming literacy, which can create a barrier for non-technical users. 
Programming literacy is currently not required of most lab personnel. This can lead to discrepancy between obtaining data and analyzing data. 

Ash aims to bridge the gap between data collection and data analysis so that anyone could use the tool. By providing an intuitive interface, 
Ash ensures that researchers, regardless of their technical background, can explore and analyse the data.

About 8% of men and 0.5% of women suffer from color vision deficiency. Color vision deficiency can make data analysis difficult for affected
population. Ash recognizes the need for inclusive software by introducing inclusive color palettes.

### Interactive Visualization Tools
Ash offers a set of visualization tools to enrich data exploration.
Researchers can visualize clusters, identify patterns, and gain insights into their data. Moreover, Ash enables users to experiment
with cluster assignment, allowing them to fine-tune the fit for their specific data.


### Ease of export
Ash streamlines the export process, allowing the end user to seamlessly save their results in various formats. 
Whether the user needs to generate reports, share findings with collaborators, or integrate results into other software, 
Ash ensures that exporting clustered data is straightforward and efficient. Read more about export options and formats
in section Exports.


# Expected Input Data Format
Out of the box, ash comes with sample data, but it is easy to replace them via the web interface.
The user must provide four files with the following information: merge matrix, joining height, order, and labels. These files are expected to be in .csv format. 
- Merge Matrix: This matrix captures the hierarchical relationships between data points. It represents the merging of clusters during the dendrogram construction. In merge matrix, there are two columns, each defines id of the clusters that are merging together at that particular point. 
In case of doubt, please refer to the r hclust documentation. 
- Joining Height: The joining height corresponds to the threshold at which clusters are merged. It plays a crucial role in defining the dendrogram structure. Is it a single column file with heights corresponding to the heights in order as is given in merge matrix.
- Order Information: The order file specifies the arrangement of data points within the dendrogram. It ensures that the hierarchy is correctly reflected.
- Labels: The labels file contains relevant annotations or identifiers for each data point. These labels enhance interpretability and context.

# How to use Ash
In Ash a dendrogam is displayed and user is expected to input points where the dendrogram should be split.
To decide about the split-points, series of supportive plots are provided.

## Uploading the data
When user wants to upload their data, they can do so by clicking on the upload button on the left side of the ui. 
The user is then met with a pop up window that will allow them to select files. The files need to be named data.csv, heights.csv, merge.csv, and order.csv. Note that Ash requires the files to be named in this manner.

![image info] (assets/examples-pictures/upload-example.png)

## Choosing palette
Choosing the preferred palette is easy in Ash. The color-blind friendly palette can be turned on via a drop down menu on the left side of Ash interface.

![image info] (assets/examples-pictures/colorblind-example.png)

## Splitting the Dendrogram
In the main screen user can input numerical label of split point, click the split button and the dendrogram will be split at that point.
The rest of the plots are updated accordingly.

#### Notes on Nodes
Nodes of dendrogram are labeled according to their height, such that the highest node is labeled with 1, second highest with 2 and so on.
From now on, we will refer to nodes by their labels. See the figure below for reference.

![Ash] (assets/enumeration.svg)

## Heatmap
A heatmap is a graphical representation of data where values are depicted using color gradients. It’s particularly useful for visualizing relationships between variables (e.g., protein levels and samples).
For better context, the heatmap is not only available as a stand-alone graph, it also connects directly to the dendrogram as can be seen on 
this example:

![image info] (assets/examples-pictures/heatmap-example.png)

By examining the heatmap, researchers can identify trends, correlations, and variations within the chosen cluster.

Heatmap is also available to the user as a stand-alone graph, where the user can explore their selected cluster. It provides a closer look at the underlying data distribution.

The heatmap can help the user to identify trends and correlations in their data. Users can discern which features exhibit similar behavior across data points. For instance, it might highlight co-expression of specific proteins among samples.


## Two features plot
The Two Features Plot allows users to visualize the relationship between two features (e.g. protein levels) using a scatter plot. This can
help with feature exploration, and finding correlation and outliers.

To use the two feature plot, the user needs to select two features from the dropdown menu. Ash then generates a scatter plot where each data point represents a sample. The x-axis corresponds to one feature, and the y-axis corresponds to the other.

To interpret the plot, the user can ask questions such as: Are there distinct patterns? Are the features positively or negatively correlated?

## Dimensionality reduction plot
The Dimensionality Reduction Plot helps the user visualize high-dimensional data in a lower-dimensional space. The user can select from
3 dimensionality reduction techniques: PCA in 2D and 3D space, t-SNE in 2D and 3D space, and UMAP.

# Exports
Ash offers convenient data export options, enhancing your flow cytometry analysis experience. Let’s explore these features:
- Cluster Export (CSV):
With a single click, users can export their final assigned clusters in CSV format.
This streamlined process ensures efficient data transfer for further analysis.

- ![image info] (assets/examples-pictures/export_csv_exampel.png)
- Graph Export:
Ash simplifies graph export by providing a one-click solution.
Users can export visualizations directly by clicking the camera icon located atop the graph.

- ![image info] (assets/examples-pictures/download_img_example.png)

