from typing import Dict, Union, Optional


import wandb
from tqdm import tqdm

# Pandas
import pandas as pd


def get_wandb_run_histories(
    project_id: str, run_filter: Dict, page_size: Optional[int] = 1000
) -> Dict[str, Union[str, Dict[str, float]]]:
    api = wandb.Api(timeout=15)
    runs = api.runs(project_id, filters=run_filter)
    run_results = {}
    for run in [r for r in runs]:
        single_run_complete_history = []
        # Get all data
        for x in tqdm(run.scan_history(page_size=page_size), desc="Loading history"):
            single_run_complete_history.append(x)
        run_results[run.id] = {
            "id": run.id,
            "name": run.name,
            "history": pd.DataFrame(single_run_complete_history),
        }
    return run_results
