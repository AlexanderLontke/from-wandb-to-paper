from typing import Any, Dict, List, Union, Optional

import pandas as pd

from from_wandb_to_paper.data.wandb_data import get_wandb_run_histories
from from_wandb_to_paper.util.data_aggregation import aggregate_run_histories
from from_wandb_to_paper.util.data_reformatting import (
    order_run_histories_by_run_names,
    aggregates_to_table,
)


def get_metrics_table(
    wandb_project_ids: Union[str, List[str]],
    run_filter: Dict[str, Any],
    run_names: List[str],
    metric_names: List[str],
    value_index: int = 0,
    value_multiplier: int = 1.0,
    page_size: int = 10000,
    verbose: bool = False,
    baselines_to_add: Optional[List[Union[Dict, pd.DataFrame]]] = None
) -> pd.DataFrame:
    # Get run histories which match the respective filter
    run_histories = get_wandb_run_histories(
        project_ids=wandb_project_ids, run_filter=run_filter, page_size=page_size
    )

    run_histories = order_run_histories_by_run_names(run_histories, run_names)

    # Remove empty run histories
    for k in [k for k, v in run_histories.items() if len(v.keys()) == 0]:
        if verbose:
            print("Dropped", k)
        run_histories.pop(k)

    # Aggregate metrics per Epoch
    lf_test_modality_aggregates = {
        modality_name: aggregate_run_histories(
            metrics_of_interest=metric_names, run_histories=modal_run_histories
        )
        for modality_name, modal_run_histories in run_histories.items()
    }
    # Reformat data to fit table format
    metrics_table = aggregates_to_table(
        lf_test_modality_aggregates,
        value_index=value_index,
        value_multiplier=value_multiplier,
    )

    # Potentially add baseline values
    if baselines_to_add is not None:
        for baseline in baselines_to_add:
            if isinstance(baseline, Dict):
                baseline = pd.DataFrame(baseline)
            metrics_table = metrics_table.join(baseline)
    return metrics_table
