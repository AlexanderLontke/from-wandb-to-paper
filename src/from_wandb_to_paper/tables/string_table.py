import abc
from abc import ABC

import pandas as pd


class StringTable(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError
