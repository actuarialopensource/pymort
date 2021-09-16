# pymort

![](./assets/demo.gif)

`pymort` is a new way to retrieve the mortality tables hosted at [https://mort.soa.org/](https://mort.soa.org/). It leverage Python types to allow you to search for and retreive the desired tables. Use `ctrl+space` to see the available types in VS Code.

## Usage

### Accessing the tables

Install pymort with `pip install pymort`. Then you can import it and load a `table` (using autocompletion as shown in the gif above).

```
import pymort

table = pymort.load(tableName="2017 Loaded CSO Composite Gender-Blended 20% Male ALB - t3282")
```

`table` is an instance of `MortalityTable`, which looks something like this. So the select table may or may not exist, if it does exist it is an instance of `SelectTable`. The ultimate table is an instance of `UltimateTable`.

```py
@dataclass
class MortalityTable:
  select: Union[None, SelectTable]
  ultimate: UltimateTable
  def rates(self, issue_age: int) -> list[float]:
    # rates takes an issue age and returns the mortality rates
    # It starts at the select rates for the issue age
    # then adds the ultimate rates for the issue age after the select period
```

If you want to get the rates for an issue age of 94:

```py
table.rates(94)
```

Which yields: `[0.09668, 0.19441,...,.95053,1.0]`

### Select tables

You can access the select table of our newly created `table` object.

```
table.select
```

This is an instance of `SelectTable`.

```py
@dataclass
class SelectTable:
  minAge: int
  maxAge: int
  minDuration: int
  maxDuration: int
  values: list[list[float]]
```

So `values` is a matrix (`list[list[float]]` technically) of dimensions `maxAge - minAge + 1` by `maxDuration - minDuration + 1`.

A few fields might need to be added in the future for certain edge cases.

### Ultimate tables

Access the ultimate table.

```
table.ultimate
```

The ultimate table is an instance of `UltimateTable`.

```
@dataclass
class UltimateTable:
  minAge: int
  maxAge: int
  values: list[float]
```

`values` is a list of mortality rates for ages `minAge` to `maxAge`.
