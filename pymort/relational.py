from dataclasses import dataclass
import importlib.resources
from . import pickled_tables
import pandas as pd
import pickle
from typing import List
from itertools import groupby

class Relational:
    """Rate tables with primary/foreign keys.

    Users can interact with mortality tables using familiar Pandas syntax.
    The primary key of the `metadata` Dataframe is a foreign key of `select` and `ultimate` Dataframes.

    Attributes:
        metadata (pd.DataFrame): Primary key of `id`. Columns are metadata describing table with `id`.
        select (pd.DataFrame): Composite primary key of `id`, `Age`, `Duration` is a MultiIndex. Column `vals` stores rates.
        metadata (pd.DataFrame): Composite primary key of `id`, `Age` is a MultiIndex. Column `vals` stores rates.

    """
    def __init__(self):
        # These pickled files are generated using `scripts/createRelational.py`.
        self.metadata: pd.DataFrame = pickle.loads(importlib.resources.read_binary(pickled_tables, 'meta.pickle'))
        self.select: pd.DataFrame = pickle.loads(importlib.resources.read_binary(pickled_tables, 'sel.pickle'))
        self.ultimate: pd.DataFrame = pickle.loads(importlib.resources.read_binary(pickled_tables, 'ult.pickle'))

@dataclass
class IdGroup:
    """
    An IdGroup is a group of IDs that have the same study and grouping in the Relational().metadata pandas table
    """
    study: str
    grouping: str
    ids: List[int]


def getIdGroup(targetId: int) -> IdGroup:
    """
    Returns an object representing the group of IDs that have the same study and grouping in the Relational().metadata pandas table.
    """
    related = Relational()
    meta = related.metadata
    meta.reset_index(inplace=True)
    # ensure that study/grouping groups are all consecutive
    meta.sort_values(by=["study", "grouping", "id"], inplace=True)
    for k, g in groupby(zip(meta.id, meta.study, meta.grouping), key=lambda x: (x[1], x[2])):
        groupIds = [x[0] for x in g]
        if targetId in groupIds:
            return IdGroup(k[0], k[1], groupIds)
    raise KeyError("Your table identifier is not in the pandas table Relational().metadata")

