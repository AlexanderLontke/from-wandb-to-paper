from typing import Literal
import pandas as pd


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
    s = getattr(metrics_table.style, f"highlight_{mode}")(
        subset=(idx[:], idx[:, "mean"]),
        axis=highlight_axis,
        props="textbf:--rwrap;",
    ).format(precision=precision)
    return s.to_latex(
        column_format="l" + "|rr" * int(len(metrics_table.columns) / 2),
        hrules=hrules,
        clines=clines,
    )
