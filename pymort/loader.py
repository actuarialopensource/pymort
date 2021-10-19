import xml.etree.ElementTree as ET
import importlib.resources
from . import archive_2021_Oct_17_051924 as data
from .tableNames import TableName
from .parser import XTbML, createXTbML
import re

def load(tableName: TableName) -> XTbML:
    id = int(re.findall(r'\d+$', tableName)[0])
    root = ET.fromstring(importlib.resources.read_text(data, f"t{id}.xml"))
    return createXTbML(root)

class PyMort:
    def __init__(self, tableName: TableName):
        self.xtbml = load(tableName)