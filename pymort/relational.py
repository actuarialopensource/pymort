import importlib.resources
from . import pickled_tables
import pandas as pd
import pickle

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

