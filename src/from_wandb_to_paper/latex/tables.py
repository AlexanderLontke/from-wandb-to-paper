from typing import Literal, Optional, Dict, List, Union
from functools import partial

import pandas as pd
import numpy as np


def highlight_second_mode(a, mode: Literal["min", "max"], props=""):
    first_max = getattr(a, mode)()
    second_max = getattr(a[a != first_max], mode)()
    return np.where(a == second_max, props, "")


def round_up_to_precision(x: float, precision: int):
    baseline = 10 ** (-precision)
    if x > baseline:
        return round(x, precision)
    elif x == 0.0:
        return x
    else:
        return baseline


def metrics_table_to_latex(
    metrics_table: pd.DataFrame,
    mode: Literal["min", "max"],
    precision: int = 2,
    hrules: bool = True,
    clines: str = "all;data",
    position: Optional[str] = "ht",
    highlight_axis: int = 1,
    index_name: Optional[str] = None,
    class_fractions: Optional[Dict[str, float]] = None,
    transpose: bool = False,
    drop_rows: Optional[List[Union[int, str]]] = None,
    round_up: bool = False,
) -> str:
    # Drop rows from table if needed
    if drop_rows is not None:
        metrics_table = metrics_table.drop(index=drop_rows)

    # Name Index
    if index_name is not None:
        metrics_table.index.rename(index_name, inplace=True)
    if class_fractions is not None:
        rename_mapping = {}
        for index_value in metrics_table.index.values:
            for class_name, class_fraction in class_fractions.items():
                if index_value.endswith(class_name):
                    rename_mapping[index_value] = f"{class_name} ({round(class_fraction*100, 1)}\\%)"
        metrics_table.rename(rename_mapping, inplace=True)

    if round_up:
        metrics_table = metrics_table.apply(lambda x: pd.Series([round_up_to_precision(x_i, precision=precision) for x_i in x]))

    idx = pd.IndexSlice
    if transpose:
        metrics_table = metrics_table.transpose()
        highlight_subset = (idx[:, "mean"], idx[:])
    else:
        highlight_subset = (idx[:], idx[:, "mean"])

    # Set style
    # Highlight highest/lowest values
    s = getattr(metrics_table.style, f"highlight_{mode}")(
        subset=highlight_subset,
        axis=highlight_axis,
        props="textbf:--rwrap;",
    ).format(precision=precision)
    s = s.apply(
        partial(highlight_second_mode, mode=mode),
        subset=highlight_subset,
        axis=highlight_axis,
        props="underline:--rwrap;",
    )
    # Highlight second highest/lowest values
    return s.to_latex(
        column_format="l" + "|rr" * int(len(metrics_table.columns) / 2),
        hrules=hrules,
        clines=clines,
        position=position,
    )

if __name__ == '__main__':
    example_data = {
        "a": [0.0000001, 0.002],
        "b": [2, 0.123],
    }

    example_data = pd.DataFrame(example_data)
    print(example_data)
    example_data = example_data.apply(lambda x: pd.Series([round_up_to_precision(x_i, precision=4) for x_i in x]))
    print(example_data)