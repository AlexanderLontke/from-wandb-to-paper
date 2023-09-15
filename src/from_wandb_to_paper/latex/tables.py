from typing import Literal
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
    highlight_axis: int = 1,
) -> str:
    idx = pd.IndexSlice
    # Set style
    # Highlight highest/lowest values
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
    )
