from abc import ABC, abstractmethod

import numpy as np
import treelog as log

from typing import List, Optional, Iterable, Tuple, Union
from .typing import Array2D

from .coords import Coords, Local
from .geometry import Patch
from .util import ensure_ncomps



PatchData = Union[Patch, List[Patch]]
FieldData = Union[Array2D, List[Array2D]]
FieldPatches = Iterable[Tuple[PatchData, FieldData]]



# Field types
# ----------------------------------------------------------------------


class FieldType:

    is_vector: bool = False
    is_displacement: bool = False
    is_geometry: bool = False
    coords: Coords = Local()

    @property
    def is_scalar(cls):
        return not cls.is_vector

class Scalar(FieldType):
    pass

class Vector(FieldType):

    is_vector = True

class Displacement(Vector):

    is_displacement = True

class Geometry(Vector):

    is_geometry = True

    def __init__(self, coords: Coords = Local()):
        self.coords = coords



# Abstract superclasses
# ----------------------------------------------------------------------


class Field(ABC):

    name: str

    # True if the field is defined on cells as opposed to nodes
    cells: bool

    # Number of components
    ncomps: int

    _fieldtype: Optional[FieldType] = None

    @abstractmethod
    def decompositions(self) -> Iterable['Field']:
        pass

    @property
    def fieldtype(self) -> FieldType:
        if self._fieldtype is None:
            return Vector() if self.ncomps > 1 else Scalar()
        return self._fieldtype

    @fieldtype.setter
    def fieldtype(self, value):
        self._fieldtype = value

    @property
    def is_scalar(self) -> bool:
        return self.fieldtype.is_scalar

    @property
    def is_vector(self) -> bool:
        return self.fieldtype.is_vector

    @property
    def is_displacement(self) -> bool:
        return self.fieldtype.is_displacement

    @property
    def is_geometry(self) -> bool:
        return self.fieldtype.is_geometry

    @property
    def coords(self) -> Coords:
        return self.fieldtype.coords

    @abstractmethod
    def patches(self, stepid: int, force: bool = False, coords: Optional[Coords] = None) -> FieldPatches:
        pass


class SourcedField(Field):
    """Utility class for creating linked chains of fields that inherit
    most but not all properties from the source field.
    """

    src: Field

    @property
    def name(self) -> str:
        return self.src.name

    @property
    def cells(self) -> bool:
        return self.src.cells

    @property
    def ncomps(self) -> int:
        return self.src.ncomps

    @property
    def fieldtype(self) -> FieldType:
        if hasattr(self, '_fieldtype') and self._fieldtype is not None:
            return self._fieldtype
        return self.src.fieldtype

    def patches(self, stepid: int, force: bool = False, coords: Optional[Coords] = None) -> FieldPatches:
        yield from self.src.patches(stepid, force=force, coords=coords)

    def decompositions(self) -> Iterable['Field']:
        yield from self.src.decompositions()



# Simple fields
# ----------------------------------------------------------------------


class SimpleField(Field):

    # True if vector fields can be decomposed to scalars
    decompose: bool

    def decompositions(self) -> Iterable['ComponentField']:
        if not self.decompose or self.ncomps == 1 or self.is_geometry:
            return
        if self.ncomps > 3:
            log.warning(f"Attempted to decompose {self.name}, ignoring extra components")
        for index, suffix in zip(range(self.ncomps), 'xyz'):
            subname = f'{self.name}_{suffix}'
            yield ComponentField(subname, self, index)


class ComponentField(SimpleField):

    ncomps = 1
    decompose = False
    fieldtype = Scalar()

    source: SimpleField
    index: int

    def __init__(self, name: str, source: Field, index: int):
        self.name = name
        self.cells = source.cells
        self.source = source
        self.index = index

    def patches(self, stepid: int, force: bool = False, coords: Optional[Coords] = None) -> FieldPatches:
        if isinstance(self.source, SimpleField):
            for patch, data in self.source.patches(stepid, force=force, coords=coords):
                yield patch, data[:, self.index : self.index+1]



# Combined field
# ----------------------------------------------------------------------


class CombinedField(Field):

    sources: List[SimpleField]

    def __init__(self, name: str, sources: List[SimpleField]):
        self.name = name

        cells = set(source.cells for source in sources)
        if len(cells) > 1:
            sources = ', '.join(source.name for source in sources)
            raise TypeError(f"Attempted to combine incompatible fields: {sources}")
        self.cells = next(iter(cells))

        self.fieldtype = None
        self.ncomps = sum(source.ncomps for source in sources)
        self.sources = sources

    def patches(self, stepid: int, force: bool = False, coords: Optional[Coords] = None) -> FieldPatches:
        subpatch_iters = zip(*(source.patches(stepid, force=force, coords=coords) for source in self.sources))
        for subpatches in subpatch_iters:
            patches, data = [], []
            for subpatch, subdata in subpatches:
                patches.append(subpatch)
                data.append(subdata)
            yield patches, data

    def decompositions(self) -> Iterable['ComponentField']:
        return; yield
