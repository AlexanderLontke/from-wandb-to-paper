from typing import Dict, List

import pandas as pd


def order_run_histories_by_run_names(run_histories: Dict, run_names: List) -> Dict:
    return {
        name: {
            run_id: run_history
            for run_id, run_history in run_histories.items()
            if run_history["name"] == name
        }
        for name in run_names
    }


def aggregates_to_table(
    run_aggregates: Dict[str, Dict[str, Dict[str, float]]],
    value_index: int,
    value_multiplier: float = 1.0,
) -> pd.DataFrame:
    dict_form = {}
    for run_name, metrics_dict in run_aggregates.items():
        for metric_name, aggregates_dict in metrics_dict.items():
            for aggregate_name, value in aggregates_dict.items():
                # Format values
                value = value[value_index] * value_multiplier
                if (run_name, aggregate_name) in dict_form.keys():
                    dict_form[(run_name, aggregate_name)][metric_name] = value
                else:
                    dict_form[(run_name, aggregate_name)] = {metric_name: value}
    return pd.DataFrame(dict_form)
