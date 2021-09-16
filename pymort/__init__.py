__version__ = '0.1.3'

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Union
import importlib.resources
from . import SOA_Tables_20210915 as data
from .tableNames import TableName
import re

@dataclass
class SelectTable:
  minAge: int
  maxAge: int
  minDuration: int
  maxDuration: int
  values: list[list[float]]

@dataclass
class UltimateTable:
  minAge: int
  maxAge: int
  values: list[float]

@dataclass
class MortalityTable:
  select: Union[None, SelectTable]
  ultimate: UltimateTable
  def rates(self, issue_age):
    if issue_age < self.select.minAge or issue_age > self.select.maxAge:
      raise ValueError('issue_age must be between {} and {}'.format(self.select.minAge, self.select.maxAge))
    if self.select is None:
      # return ultimate rates from issue_age to end of life
      return self.ultimate.values[issue_age - self.ultimate.minAge:]
    else:
      # return select rates from issue_age to end of select period, then ultimate rates from end of select period to end of life
      selectValues = self.select.values[issue_age - self.select.minAge]
      ultimateValues = self.ultimate.values[(issue_age - self.ultimate.minAge) + self.select.maxDuration:]
      return selectValues + ultimateValues

def load(tableName: TableName) -> MortalityTable:
  id = int(re.findall(r'\d+$', tableName)[0])
  root = ET.fromstring(importlib.resources.read_text(data, f"t{id}.xml"))
  values = root.findall(".//Values")

  if len(values) == 2:
    select, ultimate = values
  elif len(values) == 1:
    select, ultimate = None, values[0]
  else: 
    raise ValueError('This XML file doesn\'t have 1 or 2 <Values> elements corresponding to either select and ultimate (2 <Values>) or ultimate only (1 <Values>)')

  minScaleValues = root.findall(".//MinScaleValue")
  maxScaleValues = root.findall(".//MaxScaleValue")

  selectTable: Union[None, SelectTable] = None
  if select is not None:
    selectValues = [
        [float(value.text) for value in valuesAxis.findall('.//Y')] 
        for valuesAxis in select.findall('Axis')
    ]
    selectTable = SelectTable(
      minAge=int(minScaleValues[0].text), 
      maxAge=int(maxScaleValues[0].text), 
      minDuration=int(minScaleValues[1].text), 
      maxDuration=int(maxScaleValues[1].text), 
      values=selectValues
    )

  ultimateValues = [float(value.text) for value in ultimate.findall('.//Y')]
  # Values for ultimate come from last or first of scale values, in either case index -1 works
  ultimateTable = UltimateTable(
    minAge=int(minScaleValues[-1].text),
    maxAge=int(maxScaleValues[-1].text),
    values=ultimateValues
  )
  return MortalityTable(select=selectTable, ultimate=ultimateTable)
