import dash_bootstrap_components as dbc
from dash import dash_table, dcc, get_asset_url, html

COMMON_STYLE = {"margin": "40px"}
COMMON_PADDING = {"padding-bottom": "10px"}


with open("./assets/instructions.md", "r") as file:
    INSTRUCTION_MD = file.read()

with open("./assets/about.md", "r") as file:
    ABOUT_MD = file.read()

RECALCULATE_MERGE_MATRIX_DIV = html.Div("Data uploaded")
FAILED_UPLOAD_VALIDATION_DIV = html.Div("Data failed validation")
LOAD_MERGE_MATRIX_FROM_FILE_DIV = html.Div("Levine et. al.(2015) data loaded")


def create_layout(feature_names):
    return html.Div(
        [
            # picture credits: https://artistcoveries.wordpress.com/2019/10/13/leaf-drawing-101/
            html.Img(
                src=get_asset_url("ash_logo.png"),
                style={"width": "100%", "height": "10%"},
            ),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Instructions",
                        children=[
                            html.Div(
                                [
                                    dcc.Markdown(
                                        INSTRUCTION_MD, dangerously_allow_html=True
                                    ),
                                ],
                                style=COMMON_STYLE,
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="Interactive Clustering",
                        children=[
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H6("Custom Data:"),
                                            dcc.Upload(
                                                children=html.Div(
                                                    [
                                                        html.Button(
                                                            "Upload",
                                                            id="upload-button",
                                                            n_clicks=0,
                                                        )
                                                    ]
                                                ),
                                                multiple=True,
                                                id="upload-data",
                                            ),
                                            html.Div(id="output-data-upload"),
                                            html.H6("Colorblind Palette:"),
                                            dcc.Dropdown(
                                                [
                                                    "Colorblind palette on",
                                                    "Colorblind palette off",
                                                ],
                                                multi=False,
                                                id="colorblind-palette-dropdown",
                                                style=COMMON_PADDING,
                                            ),
                                            html.H6("Split at Node:"),
                                            dcc.Input(id="split_point", type="number"),
                                            html.H6("Assign to cluster number:"),
                                            dcc.Input(
                                                id="cluster-id", type="number", value=-1
                                            ),
                                            html.Button(
                                                "Add Split Point",
                                                id="split-button",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Remove Split Point",
                                                id="unsplit-button",
                                                n_clicks=0,
                                            ),
                                            html.Button(
                                                "Remove All Split Points",
                                                id="reset-button",
                                                n_clicks=0,
                                            ),
                                            html.Div(
                                                [
                                                    html.Br(),
                                                    html.H6(
                                                        "Assigned Clusters to CSV:"
                                                    ),
                                                    html.Button(
                                                        "Download File",
                                                        id="save-button",
                                                        n_clicks=0,
                                                    ),
                                                    html.Div(id="save-status"),
                                                    dcc.Download(id="download-data"),
                                                ]
                                            ),
                                        ],
                                        style={
                                            "float": "left",
                                            "width": "20%",
                                            "position": "sticky",
                                        },
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H1("Interactive Dendrogram"),
                                                    dcc.Graph(
                                                        id="dendrogram-custom",
                                                    ),
                                                    html.H1("Cluster-specific Heatmap"),
                                                    dcc.Dropdown(
                                                        list(feature_names),
                                                        multi=True,
                                                        id="dropdown-heatmap-plot",
                                                        value="All",
                                                    ),
                                                    dcc.Graph(
                                                        id="heatmap-graph",
                                                    ),
                                                    html.H1("Cluster Statistics"),
                                                    html.Div(
                                                        id="no-of-clusters-output"
                                                    ),
                                                    html.Div(
                                                        id="cluster-stats-table",
                                                        children=dash_table.DataTable(
                                                            id="stats_table_content"
                                                        ),
                                                    ),
                                                    dcc.RadioItems(
                                                        id="ClusterRadio",
                                                        options=[],
                                                        value="",
                                                    ),
                                                    html.Div(id="output-div"),
                                                    html.Div(id="output-div-2"),
                                                    html.Div(
                                                        id="click-output", children=""
                                                    ),
                                                    html.Div(id="min-output"),
                                                    html.Div(id="max-output"),
                                                    html.Div(id="output-div-manual"),
                                                    html.H1("Two features plot"),
                                                    html.Div(id="error-message"),
                                                    dcc.Dropdown(
                                                        list(feature_names),
                                                        multi=False,
                                                        id="dropdown-selected-features-plot-1",
                                                    ),
                                                    dcc.Dropdown(
                                                        list(feature_names),
                                                        multi=False,
                                                        id="dropdown-selected-features-plot-2",
                                                    ),
                                                    dcc.Graph(
                                                        id="two-features",
                                                    ),
                                                    html.H1(
                                                        "Dimensionality reduction plot",
                                                    ),
                                                    html.Div(
                                                        id="error-message-dim-red"
                                                    ),
                                                    dcc.Dropdown(
                                                        [
                                                            "All dimensions",
                                                            "PCA",
                                                            "PCA_3D",
                                                            "tSNE",
                                                            "tSNE_3D",
                                                            "UMAP",
                                                            "UMAP_3D",
                                                        ],
                                                        id="plot_dropdown",
                                                        value=None,
                                                    ),
                                                    dcc.Graph(
                                                        id="reduced-graph",
                                                    ),
                                                    html.Div(
                                                        id="error-message-dim-custom"
                                                    ),
                                                    dcc.Store(id="merge-matrix-memory"),
                                                    dcc.Store(id="dendrogram-memory"),
                                                    dcc.Store(
                                                        id="dendrogram-click-memory"
                                                    ),
                                                    dcc.Store(id="button-memory"),
                                                    dcc.Store(id="monocrit-list"),
                                                    dcc.Store(
                                                        id="custom-dendrogram-color-map"
                                                    ),
                                                    dcc.Store(
                                                        id="click-values-output",
                                                        data=[],
                                                    ),
                                                    dcc.Store(id="cluster-indices"),
                                                ],
                                                style=COMMON_STYLE,
                                            )
                                        ],
                                        style={"float": "right", "width": "80%"},
                                    ),
                                ]
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="About",
                        children=[
                            html.Div(
                                [
                                    dcc.Markdown(ABOUT_MD),
                                ],
                                style=COMMON_STYLE,
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
