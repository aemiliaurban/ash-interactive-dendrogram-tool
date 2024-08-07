import base64
import io

import pandas as pd


def uploaded_content_to_df(content) -> pd.DataFrame:
    content_type, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode("utf-8")))


def validate_data(df: pd.DataFrame) -> bool:
    return df.isnull().values.any()


def validate_heights(heights: list) -> bool:
    return any([not isinstance(x, (int, float)) for x in heights])


def validate_order(order: list) -> bool:
    return any([not isinstance(x, (int, float)) for x in order])


def validate_labels(labels: list) -> bool:
    return any([not isinstance(x, str) for x in labels])


def validate_merge_matrix(merge_matrix: list) -> bool:
    return any([not isinstance(x, list) for x in merge_matrix])
