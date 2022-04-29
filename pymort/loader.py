import xml.etree.ElementTree as ET
import importlib.resources
from . import archive_2021_Oct_17_051924 as data
from . import pickled_tables
from .parser import XTbML, createXTbML
import pickle
from dataclasses import dataclass
import pandas as pd

@dataclass
class Table:
    meta: pd.DataFrame
    select: pd.DataFrame
    ultimate: pd.DataFrame

def load(id: int) -> XTbML:
    root = ET.fromstring(importlib.resources.read_text(data, f"t{id}.xml"))
    return createXTbML(root)

def relational() -> Table:
    metaPickle = importlib.resources.read_binary(pickled_tables, 'meta.pickle')
    ultPickle = importlib.resources.read_binary(pickled_tables, 'ult.pickle')
    selPickle = importlib.resources.read_binary(pickled_tables, 'sel.pickle')
    return Table(pickle.loads(metaPickle), pickle.loads(selPickle), pickle.loads(ultPickle))

