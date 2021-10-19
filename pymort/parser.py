from dataclasses import dataclass
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List

@dataclass
class AxisDef:
    ScaleType: str
    AxisName: str
    MinScaleValue: int
    MaxScaleValue: int
    Increment: int

@dataclass
class MetaData:
    ScalingFactor: float
    DataType: str
    Nation: str
    TableDescription: str
    AxisDefs: List[AxisDef]

@dataclass
class Table:
    MetaData: MetaData
    Values: pd.DataFrame

@dataclass
class ContentClassification:
    TableIdentity: str
    ProviderDomain: str
    ProviderName: str
    TableReference: str
    ContentType: str
    TableName: str
    TableDescription: str
    Comments: str
    KeyWords: List[str]

@dataclass
class XTbML:
    ContentClassification: ContentClassification
    Tables: List[Table]

def createAxisDef(axisDef: ET.Element) -> AxisDef:
    '''
    Given an xml <AxisDef> element, return an AxisDef object
    '''
    return AxisDef(
        axisDef.find('./ScaleType').text,
        axisDef.find('./AxisName').text,
        int(axisDef.find('./MinScaleValue').text),
        int(axisDef.find('./MaxScaleValue').text),
        int(axisDef.find('./Increment').text)
    )

def createMetaData(metadata: ET.Element) -> MetaData:
    '''
    Given an xml <MetaData> element, return a MetaData object
    '''
    return MetaData(
        float(metadata.find('./ScalingFactor').text),
        metadata.find('./DataType').text,
        metadata.find('./Nation').text,
        metadata.find('./TableDescription').text,
        [createAxisDef(axisDef) for axisDef in metadata.findall('./AxisDef')]
    )

def constructMultiIndex(axisDefs: List[AxisDef]) -> pd.MultiIndex:
    '''
    Given a list of AxisDef objects, return the multiindex for the values dataframe.
    '''
    return pd.MultiIndex.from_product(
        [range(axisDef.MinScaleValue, axisDef.MaxScaleValue+1, axisDef.Increment) for axisDef in axisDefs],
        names=[axisDef.AxisName for axisDef in axisDefs])

def createValues(values: ET.Element, metadata: MetaData) -> pd.DataFrame:
    '''
    Given an xml <Values> element, and the table's metadata, return a multi-indexed DataFrame
    '''
    vals = [float(val.text) for val in values.iter('Y')]
    index = constructMultiIndex(metadata.AxisDefs)
    return pd.DataFrame(vals, index=index, columns=['vals'])
    
def createTable(table: ET.Element) -> Table:
    '''
    Given an xml <Table> element, return a Table object
    '''
    metaData = createMetaData(table.find('./MetaData'))
    values = createValues(table.find('./Values'), metaData)
    return Table(metaData, values)

def createContentClassification(contentClassification: ET.Element) -> ContentClassification:
    '''
    Given an xml <ContentClassification> element, return a ContentClassification object
    '''
    return ContentClassification(
        contentClassification.find('./TableIdentity').text,
        contentClassification.find('./ProviderDomain').text,
        contentClassification.find('./ProviderName').text,
        contentClassification.find('./TableReference').text,
        contentClassification.find('./ContentType').text,
        contentClassification.find('./TableName').text,
        contentClassification.find('./TableDescription').text,
        contentClassification.find('./Comments').text,
        [keyword.text for keyword in contentClassification.findall('./KeyWord')]
    )

def createXTbML(xtbml: ET.Element) -> XTbML:
    '''
    Given an xml <XTbML> element, return an XTbML object
    '''
    return XTbML(
        createContentClassification(xtbml.find('./ContentClassification')),
        [createTable(table) for table in xtbml.findall('./Table')]
    )