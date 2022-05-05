# pymort

`pymort` is a way to retrieve the mortality tables hosted at [https://mort.soa.org/](https://mort.soa.org/).

## Usage

### Installation

Install pymort with `pip install pymort`.

### Relational tables

We currently represent 2017 CSO and 2015 VBT as relational (and normalized) tables.

```py
from pymort import Relational

db = Relational()

# three Pandas tables
db.meta
db.select
db.ultimate
```

### PyXML

If you want the full details of **any** SOA table, you can use the lower level `load` API. You just need to enter the table ID.

```py
from pymort import PyXML
# load the 2017 Loaded CSO Composite Gender-Blended 20% Male ALB table (tableId = 3282)
table = PyXML(3282)
```
