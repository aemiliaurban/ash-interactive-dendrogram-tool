import pandas as pd
import numpy as np


def parse_order_df(order_raw: pd.DataFrame) -> list:
    order = order_raw.iloc[:, 0].values.tolist()
    return [x - 1 for x in order]


def parse_heights_df(heights_raw: pd.DataFrame) -> list:
    return heights_raw.iloc[:, 0].values.tolist()


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


def parse_r_hclust(merge_raw: pd.DataFrame, parsed_heights, parsed_order) -> list:
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


def iterate_linkage(linkage, start_index, nr_points, known_points):
    """
    Recursive functions which returns a tuple of point indices under a given split point or calls itself
    Known points is a tuple of points which are already known to be under a given split point. those are appended to the new tuple
    """
    if start_index < nr_points:
        return known_points + (int(start_index),)

    else:
        reversed_index = int(start_index - nr_points)
        left = linkage[reversed_index][0]
        right = linkage[reversed_index][1]

        return iterate_linkage(
            linkage, left, nr_points, known_points
        ) + iterate_linkage(linkage, right, nr_points, known_points)


def split_dendrogram(
    link_mat: np.ndarray, split_points: list[int], cluster_ids: list[int]
):
    next_cluster_index = 0
    nr_points = link_mat.shape[0] + 1
    initial_cluster_assignments = [next_cluster_index] * nr_points
    user_defined_cluster_indices = iter(cluster_ids)

    # linkage matrix is sorted by distance
    for point in split_points:
        next_cluster_index = next(user_defined_cluster_indices)
        reversed_index = int(nr_points - point - 1)
        left = link_mat[reversed_index][0]
        right = link_mat[reversed_index][1]

        indices = iterate_linkage(link_mat, left, nr_points, tuple()) + iterate_linkage(
            link_mat, right, nr_points, tuple()
        )

        for index in indices:
            initial_cluster_assignments[index] = next_cluster_index

    return initial_cluster_assignments
