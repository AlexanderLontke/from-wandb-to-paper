from typing import Literal, Optional, Dict
from functools import partial

import pandas as pd
import numpy as np


def highlight_second_mode(a, mode: Literal["min", "max"], props=""):
    first_max = getattr(a, mode)()
    second_max = getattr(a[a != first_max], mode)()
    return np.where(a == second_max, props, "")


def metrics_table_to_latex(
    metrics_table: pd.DataFrame,
    mode: Literal["min", "max"],
    precision: int = 2,
    hrules: bool = True,
    clines: str = "all;data",
    position: str = "ht",
    highlight_axis: int = 1,
    index_name: Optional[str] = None,
    class_fractions: Optional[Dict[str, float]] = None,
) -> str:
    # Name Index
    if index_name is not None:
        metrics_table.index.rename(index_name, inplace=True)
    if class_fractions is not None:
        rename_mapping = {}
        for index_value in metrics_table.index.values:
            for class_name, class_fraction in class_fractions.items():
                if index_value.endswith(class_name):
                    rename_mapping[index_value] = f"{class_name} ({round(class_fraction*100, 1)}%)"
        metrics_table.rename(rename_mapping)

    # Set style
    # Highlight highest/lowest values
    idx = pd.IndexSlice
    s = getattr(metrics_table.style, f"highlight_{mode}")(
        subset=(idx[:], idx[:, "mean"]),
        axis=highlight_axis,
        props="textbf:--rwrap;",
    ).format(precision=precision)
    s = s.apply(
        partial(highlight_second_mode, mode=mode),
        subset=(idx[:], idx[:, "mean"]),
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
