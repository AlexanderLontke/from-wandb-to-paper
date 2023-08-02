import pandas as pd


def metrics_table_to_latex(
    metrics_table: pd.DataFrame,
    precision: int = 2,
    hrules: bool = True,
    clines: str = "all;data",
    highlight_max_axis: int = 1,
) -> str:
    idx = pd.IndexSlice
    # Set style
    s = metrics_table.style.highlight_max(
        subset=(idx[:], idx[:, "mean"]),
        axis=highlight_max_axis,
        props="textbf:--rwrap;",
    ).format(precision=precision)
    return s.to_latex(
        column_format="l" + "|rr" * int(len(metrics_table.columns) / 2),
        hrules=hrules,
        clines=clines,
    )
