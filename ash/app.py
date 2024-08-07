import copy
from collections import Counter
from unittest.mock import patch

import matplotlib.pyplot
import pandas as pd
import plotly.graph_objects as go
from dash import (Dash, Input, Output, State, ctx, dash_table, dcc,
                  get_asset_url, html)
from plotly.subplots import make_subplots

from common.custom_data_utils import uploaded_content_to_df
from common.custom_threshold_plotly_dendrogram import \
    create_dendrogram_modified
from common.data_parser import (RDataParser, parse_heights_df, parse_merge_df,
                                parse_order_df)
from common.plot_master import PlotMaster
from common.util import (assign_clusters, convert_to_dict,
                         plot_input_data_reduced, write_to_text_file)
from layout import (LOAD_MERGE_MATRIX_FROM_FILE_DIV,
                    RECALCULATE_MERGE_MATRIX_DIV, create_layout)

matplotlib.pyplot.switch_backend("agg")

r = RDataParser()
r.parse()

app = Dash(__name__)
feature_names = r.dataset.columns
app.layout = create_layout(feature_names)
server = app.server


# reset dropdown-heatmap-plot when new data are uploaded
@app.callback(
    Output("dropdown-heatmap-plot", "value"),
    Input("output-data-upload", "children"),
    prevent_initial_call=True,
)
def reset_heatmap_feature(_):
    return None


# reset dropdown-selected-features-plot-1 and dropdown-selected-features-plot-2 when new data are uploaded
@app.callback(
    Output("dropdown-selected-features-plot-1", "value"),
    Output("dropdown-selected-features-plot-2", "value"),
    Input("output-data-upload", "children"),
    prevent_initial_call=True,
)
def reset_two_features(_):
    return None, None


# reset plot_dropdown for dimensionality reduction algos when new data are uploaded
@app.callback(
    Output("plot_dropdown", "value"),
    Input("output-data-upload", "children"),
    prevent_initial_call=True,
)
def reset_dim_red_algo(_):
    return None


@app.callback(
    Output("merge-matrix-memory", "data"),
    Output("output-data-upload", "children"),
    Output("dropdown-heatmap-plot", "options"),
    Output("dropdown-selected-features-plot-1", "options"),
    Output("dropdown-selected-features-plot-2", "options"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def load_custom_data(contents, list_of_names):

    default_data = {
        "merge_matrix": r.merge_matrix,
        "dataset": r.dataset.to_json(date_format="iso", orient="split"),
        "labels": r.labels,
        "order": r.order,
    }

    if [contents, list_of_names] == [None, None]:
        return (
            default_data,
            LOAD_MERGE_MATRIX_FROM_FILE_DIV,
            r.dataset.columns,
            r.dataset.columns,
            r.dataset.columns,
        )

    files = {}
    for content, name in zip(contents, list_of_names):
        files[name] = uploaded_content_to_df(content)

    parsed_heights = parse_heights_df(files["heights.csv"])
    parsed_order = parse_order_df(files["order.csv"])
    custom_data = {
        "merge_matrix": parse_merge_df(
            files["merge.csv"], parsed_heights, parsed_order
        ),
        "dataset": files["data.csv"].to_json(date_format="iso", orient="split"),
        "labels": [i for i in range(len(parsed_order))],
        "order": parsed_order,
    }

    return (
        custom_data,
        RECALCULATE_MERGE_MATRIX_DIV,
        files["data.csv"].columns,
        files["data.csv"].columns,
        files["data.csv"].columns,
    )


@app.callback(
    [
        Output("monocrit-list", "data"),
        Output("cluster-indices", "data"),
        Output("cluster-id", "value"),
    ],
    [
        Input("monocrit-list", "data"),
        Input("split-button", "n_clicks"),
        Input("unsplit-button", "n_clicks"),
        Input("reset-button", "n_clicks"),
        Input("dendrogram-click-memory", "data"),
        Input("merge-matrix-memory", "data"),
        State("cluster-indices", "data"),
        State("cluster-id", "value"),
        State("split_point", "value"),
    ],
)
def add_split_point(
    monocrit_split_points,
    split_button_clicks,
    unsplit_button_clicks,
    reset_button_clicks,
    dendrogram_click_data,
    merge_matrix_json,
    cluster_indices,
    cluster_id,
    split_point_value,
):
    if not monocrit_split_points:
        monocrit_split_points = []
        cluster_indices = []
    if ctx.triggered_id == "merge-matrix-memory":
        # reset when new data are uploaded
        return [], [], 1
    elif ctx.triggered_id == "split-button":
        # add cluster index to monocrit list
        monocrit_split_points.append(int(split_point_value))
        cluster_indices.append(int(cluster_id))

    elif ctx.triggered_id == "unsplit-button":
        cluster_indices = [
            cluster_id
            for point, cluster_id in zip(monocrit_split_points, cluster_indices)
            if point != split_point_value
        ]
        monocrit_split_points = [
            point for point in monocrit_split_points if point != split_point_value
        ]

    elif ctx.triggered_id == "reset-button":
        monocrit_split_points = []
        cluster_indices = []

    elif ctx.triggered_id == "dendrogram-click-memory":
        if dendrogram_click_data is not None:
            label = dendrogram_click_data["points"][0]["hovertext"]
            _, node_nr = label.split(" ")

            monocrit_split_points.append(int(node_nr))
            cluster_indices.append(int(cluster_id))
    try:
        next_cluster_label = max(cluster_indices) + 1
    except:
        next_cluster_label = 1
    return monocrit_split_points, cluster_indices, next_cluster_label


@app.callback(
    Output("dendrogram-custom", "figure"),
    [
        Input("merge-matrix-memory", "data"),
        Input(
            "dendrogram-memory", "data"
        ),
        Input("dropdown-heatmap-plot", "value"),
        Input("colorblind-palette-dropdown", "value"),
    ],
)
def plot_dendrogram(
    merge_matrix_json, data, heatmap_features, colorblind_palette_input
):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0)
    dendrogram = go.Figure(data=data["data"], layout=data["layout"])

    for trace in dendrogram.data:
        fig.add_trace(trace, row=1, col=1)
    fig.update_layout(data["layout"])

    # get the minimum and maximum x axis values across all traces
    x_min = min([min(trace["x"]) for trace in dendrogram.data])
    x_max = max([max(trace["x"]) for trace in dendrogram.data])
    y_min = min([min(trace["y"]) for trace in dendrogram.data])
    y_max = max([max(trace["y"]) for trace in dendrogram.data])

    fig.update_layout(xaxis_range=[x_min, x_max])
    fig.update_layout(yaxis_range=[y_min, y_max * 1.1])

    plot_master = PlotMaster(
        pd.read_json(merge_matrix_json["dataset"], orient="split"),
        data["labels"],
        merge_matrix_json["order"],
        data["leaves_color_map_translated"],
    )
    dataset = pd.read_json(merge_matrix_json["dataset"], orient="split")
    dataset["dendrogram_order"] = merge_matrix_json["order"]
    dataset = dataset.sort_values(by="dendrogram_order")
    dataset = dataset.drop(columns=["dendrogram_order"])

    try:
        colorblind_palette = (
            True if colorblind_palette_input == "Colorblind palette on" else False
        )
        if colorblind_palette:
            colorscale = "GnBu"
        else:
            colorscale = None
        heatmap = go.Figure(
            data=go.Heatmap(
                plot_master.df_to_plotly(dataset, heatmap_features),
                colorbar={"title": "Feature Value"},
                colorscale=colorscale,
            )
        )
    except KeyError:
        heatmap = go.Figure()

    for trace in heatmap.data:
        fig.add_trace(trace, row=2, col=1)
    fig.update_layout(data["layout"])

    return fig


@app.callback(
    Output("dendrogram-click-memory", "data"), Input("dendrogram-custom", "clickData")
)
def store_dendrogram_click(clickData):
    return clickData


@app.callback(
    Output("dendrogram-memory", "data"),
    Input("colorblind-palette-dropdown", "value"),
    Input("monocrit-list", "data"),
    Input("cluster-indices", "data"),
    Input(
        "merge-matrix-memory", "data"
    ),  # triggered when new data are uploaded i.e. merge matrix is recalculated
)
def create_dendrogram(
    colorblind_palette_input, monocrit_list, cluster_ids, merge_matrix_json
):
    """
    Dendrogram initialization
    """
    colorblind_palette = (
        True if colorblind_palette_input == "Colorblind palette on" else False
    )
    with patch(
        "plotly.figure_factory._dendrogram._Dendrogram.get_dendrogram_traces",
        new=create_dendrogram_modified,
    ) as create_dendrogram:
        custom_dendrogram = create_dendrogram(
            merge_matrix_json["merge_matrix"],
            labels=merge_matrix_json["labels"],
            colorblind_palette=colorblind_palette,
            monocrit_list=monocrit_list,
            cluster_ids=cluster_ids,
        )
        assigned_clusters = convert_to_dict(
            assign_clusters(custom_dendrogram.leaves_color_map_translated)
        )
        write_to_text_file("custom_dendrogram.txt", custom_dendrogram.dendro)

        return {
            "dendro": custom_dendrogram.dendro,
            "leaves_color_map_translated": custom_dendrogram.leaves_color_map_translated,
            "clusters": custom_dendrogram.clusters,
            "labels": custom_dendrogram.labels,
            "data": custom_dendrogram.data,
            "layout": custom_dendrogram.layout,
            "icoord": custom_dendrogram.xvals,
            "dcoord": custom_dendrogram.yvals,
            "assigned_clusters": assigned_clusters,
            "monocrit_list": monocrit_list,
            "cluster_indices": custom_dendrogram.cluster_indices,
            "color_map": custom_dendrogram.color_map,
        }


@app.callback(
    Output("no-of-clusters-output", "children"), Input("dendrogram-memory", "data")
)
def get_number_of_clusters(data):
    return f"Number of clusters: {data['clusters']}"


@app.callback(
    Output(component_id="cluster-stats-table", component_property="children"),
    [Input("dendrogram-memory", "data")],
)
def update_cluster_stats_table(data):
    counts_per_cluster = Counter(data["cluster_indices"])
    cluster_indices_labels = list(set(data["cluster_indices"]))
    table_data = [
        {
            "Cluster ID": i,
            "Number of Samples": counts_per_cluster[i],
            "Share of Samples": round(
                counts_per_cluster[i] / sum(counts_per_cluster.values()), 2
            ),
            "Cluster Colour": "",
        }
        for i in sorted(counts_per_cluster)
    ]
    table = dash_table.DataTable(
        id="stats_table_content",
        data=table_data,
        row_selectable="single",
        selected_rows=[0],
        style_data_conditional=[
            {
                "if": {"row_index": i, "column_id": "Cluster Colour"},
                "background-color": data["color_map"][str(cluster_indices_labels[i])],
            }
            for i in range(len(counts_per_cluster))
        ],
    )
    return html.Div(id="cluster-stats-table", children=table)


@app.callback(
    Output("heatmap-graph", "figure"),
    Input("dropdown-heatmap-plot", "value"),
    Input("dendrogram-memory", "data"),
    Input("stats_table_content", "selected_rows"),
    Input("stats_table_content", "data"),
    Input("colorblind-palette-dropdown", "value"),
    Input("merge-matrix-memory", "data"),
)
def plot_heatmap(
    value,
    data,
    selected_rows: list[int],
    table_data,
    colorblind_palette_input,
    merge_matrix_json,
):
    plot_master = PlotMaster(
        pd.read_json(merge_matrix_json["dataset"], orient="split"),
        data["labels"],
        merge_matrix_json["order"],
        data["leaves_color_map_translated"],
    )
    try:
        selected_cluster_label = table_data[selected_rows[0]]["Cluster ID"]
        mask = [i == selected_cluster_label for i in data["cluster_indices"]]
        data_subset = (
            pd.read_json(merge_matrix_json["dataset"], orient="split")
            .loc[mask, :]
            .reset_index(drop=True)
        )

        colorblind_palette = (
            True if colorblind_palette_input == "Colorblind palette on" else False
        )
        if colorblind_palette:
            colorscale = "GnBu"
        else:
            colorscale = None

        fig = go.Figure(
            data=go.Heatmap(
                plot_master.df_to_plotly(data_subset, value),
                colorscale=colorscale,
                colorbar={"title": "Feature Value"},
            )
        )
        fig.update_layout({"xaxis_title": "Observation Number"})
        # empty name prevents trace name from being displayed in the hover tooltip
        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "Observation Number: %{x}",
                    "Feature Name: %{y}",
                ]
            ),
            name="",
        )

        return fig
    except:
        # nothing selected, no need to handle, returning empty figure
        return go.Figure()


@app.callback(
    Output("two-features", "figure"),
    Output("error-message", "children"),
    Input("dropdown-selected-features-plot-1", "value"),
    Input("dropdown-selected-features-plot-2", "value"),
    Input("dendrogram-memory", "data"),
    Input("merge-matrix-memory", "data"),
    prevent_initial_call=True,
)
def plot_two_selected_features(f1, f2, data, merge_matrix_json):
    try:
        color_mask = [data["color_map"][str(i)] for i in data["cluster_indices"]]
        features = [f1, f2]
        if f1 == f2 and f1 is not None and f2 is not None:
            feature_plot = go.Figure()
            error_message = html.Div(
                [
                    html.Img(
                        src=get_asset_url("warn_symbol.png"),
                        style={"display": "inline-block", "height": "100px"},
                    ),
                    html.Div(
                        "Please select two different features.",
                        style={"display": "inline-block", "height": "100px"},
                    ),
                ]
            )
        else:
            color_map = copy.deepcopy(data["leaves_color_map_translated"])
            plot_master = PlotMaster(
                pd.read_json(merge_matrix_json["dataset"], orient="split"),
                merge_matrix_json["labels"],
                merge_matrix_json["order"],
                color_map,
            )
            feature_plot = plot_master.plot_selected_features(features, color_mask)
            feature_plot.update_layout({"xaxis_title": f1, "yaxis_title": f2})
            feature_plot.update_traces(
                hovertemplate="<br>".join(
                    [
                        f"{f1}: %{{x}}",
                        f"{f2}: %{{y}}",
                    ]
                ),
                name="",
            )
            error_message = None
    except Exception:
        # Empty result
        feature_plot = go.Figure()
        error_message = None

    return feature_plot, error_message


@app.callback(
    Output("reduced-graph", "figure"),
    Output("error-message-dim-red", "children"),
    Input("plot_dropdown", "value"),
    Input("dendrogram-memory", "data"),
    Input("ClusterRadio", "value"),
    Input("merge-matrix-memory", "data"),
)
def plot_data_reduced(value, data, highlight_area, merge_matrix_json):
    if value is None:
        reduced_plot = go.Figure()
        error_message = (
            "Please select dimensionality reduction.\n "
            "Ash will attempt to access pre-calculated dimensionality reduction data at the designated location (ash/common/user_data/reduced_dimensions)."
            "If the data is not found, "
            "Ash will perform the necessary calculations on the matrix data provided at the designated location (ash/common/user_data/data.csv), "
            "which may result in longer processing time."
        )
    else:
        color_map = copy.deepcopy(data["leaves_color_map_translated"])
        color_mask = [data["color_map"][str(i)] for i in data["cluster_indices"]]
        plot_master = PlotMaster(
            pd.read_json(merge_matrix_json["dataset"], orient="split"),
            merge_matrix_json["labels"],
            merge_matrix_json["order"],
            color_map,
        )
        reduced_plot = plot_input_data_reduced(value, plot_master, color_mask)
        error_message = None

    return reduced_plot, error_message


@app.callback(
    Output("download-data", "data"),
    State("dendrogram-memory", "data"),
    State("merge-matrix-memory", "data"),
    Input("save-button", "n_clicks"),
    prevent_initial_call=True,
)
def save_file(data, merge_matrix_json, n_clicks):
    if n_clicks != 0:
        return dcc.send_data_frame(
            pd.concat(
                [
                    pd.read_json(merge_matrix_json["dataset"], orient="split"),
                    pd.DataFrame({"ASSIGNED_CLUSTER": data["cluster_indices"]}),
                ],
                axis=1,
            ).to_csv,
            "assigned_clusters.csv",
        )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, dev_tools_silence_routes_logging=False)
