import importlib.resources
from . import pickled_tables
import pandas as pd

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
        self.metadata: pd.DataFrame = importlib.resources.read_binary(pickled_tables, 'meta.pickle')
        self.select: pd.DataFrame = importlib.resources.read_binary(pickled_tables, 'sel.pickle')
        self.ultimate: pd.DataFrame = importlib.resources.read_binary(pickled_tables, 'ult.pickle')

