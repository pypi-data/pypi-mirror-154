# tinykit

A toolkit for TinyDB with additional features (transaction, model, etc).

## Installation

    pip install tinykit

## Quickstart

Plain Python ``dict``:

```python
from tinykit import Database


db = Database("/path/to/db.json")
table = db.table("testing")

with db.transaction(table) as tr:
    tr.insert({"label": "database"})

table.get(db.where("label") == "database")
```

With ``tinykit.Model`` object:

```python
from jsonmodels.fields import StringField
from tinykit import Database
from tinykit import Model


class TestingModel(Model):
    __tablename__ = "testing"
    label = StringField()

model = TestingModel()
model.label = "database"

db = Database("/path/to/db.json")
table = db.table(model.__tablename__)

with db.transaction(table) as tr:
    tr.insert(model.to_struct())

table.get(db.where("label") == model.label)
```
