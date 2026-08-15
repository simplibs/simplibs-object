from .ClassMethodProtocol import FunctionProtocol, ClassMethodProtocol
from .LogicSignature import LogicSignature, P, R

_DESIGN_NOTES = """
# Methods Protocols Sub-Package

## Purpose
Provides structural protocols and type anchors for method introspection, bound classmethod validation,
and ParamSpec signature propagation across composite calculation decorators.

## Internal Components Registry

| Component              | Type     | Description                                                               |
| :--------------------- | :------- | :------------------------------------------------------------------------ |
| `FunctionProtocol`     | Protocol | Auxiliary protocol matching underlying function object (`__func__`).       |
| `ClassMethodProtocol`  | Protocol | Protocol for bound classmethods used during metadata introspection.        |
| `LogicSignature`       | Protocol | Generic anchor class preserving `_logic` parameters (`P`) and return (`R`).|
"""