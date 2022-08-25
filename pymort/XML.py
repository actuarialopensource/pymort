from dataclasses import dataclass
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List
import importlib.resources
from . import archive_2022_May_04_093934 as data

# The following classes represent the xml elements in the XTbML file https://mort.soa.org/About.aspx


@dataclass
class AxisDef:
    """
    Corresponds to the XML element having the same name.
    """

    ScaleType: str
    AxisName: str
    MinScaleValue: int
    MaxScaleValue: int
    Increment: int


@dataclass
class MetaData:
    """
    Corresponds to the XML element having the same name.
    """

    ScalingFactor: float
    DataType: str
    Nation: str
    TableDescription: str
    AxisDefs: List[AxisDef]


@dataclass
class Table:
    """
    Corresponds to the XML element having the same name.
    """

    MetaData: MetaData
    Values: pd.DataFrame


@dataclass
class ContentClassification:
    """
    Corresponds to the XML element having the same name.
    """

    TableIdentity: int
    ProviderDomain: str
    ProviderName: str
    TableReference: str
    ContentType: str
    TableName: str
    TableDescription: str
    Comments: str
    KeyWords: List[str]


class MortXML:
    """A Python wrapper for XML mortality tables.

    A tree of nested Python classes that represent an `XML standard <https://mort.soa.org/About.aspx/>`_
    used by tables hosted at `mort.soa.org <https://mort.soa.org/>`_.

    Corresponds to the `XTbML` root element in the XML file.

    Attributes:
        contentClassification (ContentClassification): Corresponds to ContentClassification XML element.
        tables (List[Table]): Corresponds to Table XML elements.

    """

    def __init__(self, id: int):
        """
        Takes the id of a table and returns the PyXML object.

        Args:
            id (int): The id of the table to be loaded.
        """
        root = ET.fromstring(importlib.resources.read_text(data, f"t{id}.xml"))
        self.ContentClassification: ContentClassification = createContentClassification(
            root.find("./ContentClassification")
        )
        self.Tables: List[Table] = createTables(root)


# The following functions turn XML elements into Python objects.


def createAxisDef(axisDef: ET.Element) -> AxisDef:
    """
    Given an xml <AxisDef> element, return an AxisDef object
    """
    return AxisDef(
        axisDef.find("./ScaleType").text,
        axisDef.find("./AxisName").text,
        int(axisDef.find("./MinScaleValue").text),
        int(axisDef.find("./MaxScaleValue").text),
        int(axisDef.find("./Increment").text),
    )


def createMetaData(metadata: ET.Element) -> MetaData:
    """
    Given an xml <MetaData> element, return a MetaData object
    """
    return MetaData(
        float(metadata.find("./ScalingFactor").text),
        metadata.find("./DataType").text,
        metadata.find("./Nation").text,
        metadata.find("./TableDescription").text,
        [createAxisDef(axisDef) for axisDef in metadata.findall("./AxisDef")],
    )


def getAxisVals(axis: ET.Element) -> pd.DataFrame:
    """
    Take the bottom level `Axis` tag (having no "t" attribute).
    Return two lists of the same length, containing the "t" attribute and the float(tag.text)
    """
    ys = list(axis.iter("Y"))
    # check for y.text is for triangular tables
    ts = [int(y.attrib["t"]) for y in ys if y.text]
    vals = [float(y.text) for y in ys if y.text]
    # this means the table is two dimensional
    if "t" in axis.attrib:
        rowT = int(axis.attrib["t"])
        colTs = ts
        df = pd.DataFrame({"Age": [rowT] * len(vals), "Duration": colTs, "vals": vals})
        df.set_index(["Age", "Duration"], inplace=True)
        return df
    else:  # one dimensional
        df = pd.DataFrame({"Age": ts, "vals": vals})
        df.set_index("Age", inplace=True)
        return df


def createValues(table: ET.Element) -> pd.DataFrame:
    """
    Take the top level `Table` tag and return a list
    """
    axes = table.findall("./Values/Axis")
    dfs = []
    for axis in axes:
        dfs.append(getAxisVals(axis))
    return pd.concat(dfs)


def createTable(table: ET.Element) -> Table:
    """
    Given an xml <Table> element, return a Table object
    """
    metaData = createMetaData(table.find("./MetaData"))
    values = createValues(table)
    return Table(metaData, values)


def createTables(root: ET.Element) -> List[Table]:
    """Given the root of an xml tree, return a list of Table objects"""
    return [createTable(table) for table in root.findall("./Table")]


def createContentClassification(
    contentClassification: ET.Element,
) -> ContentClassification:
    """
    Given an xml <ContentClassification> element, return a ContentClassification object
    """
    return ContentClassification(
        int(contentClassification.find("./TableIdentity").text),
        contentClassification.find("./ProviderDomain").text,
        contentClassification.find("./ProviderName").text,
        contentClassification.find("./TableReference").text,
        contentClassification.find("./ContentType").text,
        contentClassification.find("./TableName").text,
        contentClassification.find("./TableDescription").text,
        contentClassification.find("./Comments").text,
        [keyword.text for keyword in contentClassification.findall("./KeyWord")],
    )
