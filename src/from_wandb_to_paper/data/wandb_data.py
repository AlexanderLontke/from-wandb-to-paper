from typing import List, Dict, Union, Optional


import wandb
from tqdm import tqdm

# Pandas
import pandas as pd


def get_wandb_run_histories(
    project_ids: Union[str, List[str]], run_filter: Dict, page_size: Optional[int] = 1000
) -> Dict[str, Union[str, Dict[str, float]]]:
    api = wandb.Api(timeout=15)
    if isinstance(project_ids, str):
        project_ids = [project_ids]
    run_results = {}
    for project_id in project_ids:
        runs = api.runs(project_id, filters=run_filter)
        for run in tqdm([r for r in runs], desc="Loading history"):
            single_run_complete_history = []
            # Get all data
            for x in run.scan_history(page_size=page_size):
                single_run_complete_history.append(x)
            run_results[run.id] = {
                "id": run.id,
                "name": run.name,
                "history": pd.DataFrame(single_run_complete_history),
            }
    return run_results
