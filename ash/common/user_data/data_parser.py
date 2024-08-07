import os

import pandas as pd

DATA_FOLDER = os.path.join(os.getcwd(), "common", "user_data")
DATA_FOLDER = "/app/ash/common/user_data"


class RDataParser:
    def __init__(self):
        self.dataset = self.read_dataset()
        self.merge_matrix = [map(float, x) for x in self.read_merge_matrix()]
        self.joining_height = [float(x) for x in self.read_joining_height()]
        self.order = [float(x) for x in self.read_order_data()]
        self.labels = self.read_labels()

    @staticmethod
    def read_dataset():
        return pd.read_csv(os.path.join(DATA_FOLDER, "data.csv"))

    @staticmethod
    def read_order_data():
        order_raw = pd.read_csv(os.path.join(DATA_FOLDER, "order.csv"))[
            "x"
        ].values.tolist()
        order = [x - 1 for x in order_raw]
        return order

    @staticmethod
    def read_joining_height():
        return pd.read_csv(os.path.join(DATA_FOLDER, "heights.csv"))[
            "x"
        ].values.tolist()

    @staticmethod
    def read_merge_matrix():
        merge_matrix_raw = pd.read_csv(os.path.join(DATA_FOLDER, "merge.csv"))
        merge_matrix_V1 = merge_matrix_raw["V1"].values.tolist()
        merge_matrix_V2 = merge_matrix_raw["V2"].values.tolist()
        merge_matrix = [list(x) for x in zip(merge_matrix_V1, merge_matrix_V2)]
        return merge_matrix

    def read_labels(self):
        try:
            labels = pd.read_csv(os.path.join(DATA_FOLDER, "labels.csv"))
        except FileNotFoundError:
            labels = [i for i in range(len(self.order))]
        return labels

    def convert_merge_matrix(self):
        transformed_matrix = []
        for node in self.merge_matrix:
            new_node = []
            for el in node:
                if el < 0:
                    transformed_el = abs(el) - 1
                else:
                    transformed_el = el + len(self.merge_matrix)
                new_node.append(transformed_el)
            transformed_matrix.append(new_node)

        self.merge_matrix = transformed_matrix

    def add_joining_height(self):
        for index in range(len(self.merge_matrix)):
            self.merge_matrix[index].append(self.joining_height[index])
            self.merge_matrix[index].append(self.order[index])

    def parse(self):
        self.convert_merge_matrix()
        self.add_joining_height()


def merge_matrix_from_R_to_scipy_format(merge_matrix: list) -> list:
    scipy_matrix = []
    for row in merge_matrix:
        new_node = []
        for element in row:
            if element < 0:
                transformed_el = abs(element) - 1
            else:
                transformed_el = element + len(merge_matrix)
            new_node.append(transformed_el)
        scipy_matrix.append(new_node)
    return scipy_matrix


def parse_merge_df(merge_raw: pd.DataFrame, parsed_heights, parsed_order) -> list:
    print(merge_raw.head())
    first_col = merge_raw.iloc[:, 0].values.tolist()
    second_col = merge_raw.iloc[:, 1].values.tolist()
    merge_matrix_as_list = [
        [float(x_1), float(x_2)] for x_1, x_2 in zip(first_col, second_col)
    ]

    merge_matrix = merge_matrix_from_R_to_scipy_format(merge_matrix_as_list)

    for i in range(len(merge_matrix)):
        merge_matrix[i].append(parsed_heights[i])
        merge_matrix[i].append(parsed_order[i])

    return merge_matrix


def parse_order_df(order_raw: pd.DataFrame) -> list:
    order = order_raw.iloc[:, 0].values.tolist()
    return [x - 1 for x in order]


def parse_heights_df(heights_raw: pd.DataFrame) -> list:
    return heights_raw.iloc[:, 0].values.tolist()
