# pymort

`pymort` is a way to retrieve the mortality tables hosted at [https://mort.soa.org/](https://mort.soa.org/).

## Usage

### Installation

Install pymort with `pip install pymort`.

### Relational tables

We currently represent 2017 CSO and 2015 VBT as relational (and normalized) tables.

```py
import pymort

db = pymort.relational()

# three Pandas tables
db.meta
db.select
db.ultimate
```

### XTbML

If you want the full details of **any** SOA table, you can use the lower level `load` API. You just need to enter the table ID.

```py
import pymort
# load the 2017 Loaded CSO Composite Gender-Blended 20% Male ALB table
table = pymort.load(tableName=3282)
```

`pymort.load` returns an instance of `XTbML`. XTbML is an XML standard for representing the tables at [mort.soa.org](https://mort.soa.org/), and the `XTbML` object is a Python class that mirrors the XML structure. At the bottom of the following code you can see the definition of the `XTbML` class. The attributes of the class are the children of the XML element. **Notice the Table class contains a pd.DataFrame, these are the rates!**. Use intellisense to navigate the class.

```py
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
```
