from dataclasses import dataclass
from typing import Optional, Type


@dataclass(kw_only=True)
class BaseField:
    nullable: bool = False

    @classmethod
    def typename(cls):
        return cls.__name__

    @classmethod
    def subfields(cls) -> list[tuple[str, "BaseField"]]:
        return []


@dataclass(kw_only=True)
class StringField(BaseField):
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    regex: Optional[str] = None

    @property
    def has_min_length(self):
        return self.min_length is not None

    @property
    def has_max_length(self):
        return self.max_length is not None

    @property
    def has_regex(self):
        return self.regex is not None


@dataclass(kw_only=True)
class IntegerField(BaseField):
    min: Optional[int] = None
    max: Optional[int] = None

    @property
    def has_min(self):
        return self.min is not None

    @property
    def has_max(self):
        return self.max is not None


@dataclass(kw_only=True)
class FloatField(BaseField):
    min: Optional[float] = None
    max: Optional[float] = None

    @property
    def has_min(self):
        return self.min is not None

    @property
    def has_max(self):
        return self.max is not None


@dataclass(kw_only=True)
class BooleanField(BaseField):
    pass


@dataclass(kw_only=True)
class ArrayField(BaseField):
    items: BaseField


class Compound(BaseField):
    @classmethod
    def subfields(cls) -> list[tuple[str, BaseField]]:
        return [
            (attr_name, attr)
            for attr_name, attr in ((attr_name, getattr(cls, attr_name)) for attr_name in dir(cls))
            if isinstance(attr, BaseField)
        ]


PRIMITIVES = (ArrayField, StringField, IntegerField, FloatField, BooleanField)


def is_array_field(field: BaseField):
    return isinstance(field, ArrayField)


def is_string_field(field: BaseField):
    return isinstance(field, StringField)


def is_integer_field(field: BaseField):
    return isinstance(field, IntegerField)


def is_float_field(field: BaseField):
    return isinstance(field, FloatField)


def is_numeric_field(field: BaseField):
    return isinstance(field, (IntegerField, FloatField))


def is_boolean_field(field: BaseField):
    return isinstance(field, BooleanField)


def is_primitive_field_type(field: type):
    return issubclass(field, PRIMITIVES)


def is_primitive_field(field: BaseField):
    return is_primitive_field_type(type(field))


def is_pure_primitive_field_type(field: type):
    return field in PRIMITIVES


def is_pure_primitive_field(field: BaseField):
    return is_pure_primitive_field_type(type(field))


def gather_dependencies(compound: type) -> set[type]:
    compounds = [compound]
    result: set[Type[Compound]] = set()
    while compounds:
        q, compounds = compounds[0], compounds[1:]
        if q in result:
            continue
        result.add(q)
        for _, subfield in q.subfields():
            while isinstance(subfield, ArrayField):
                subfield = subfield.items
            if type(subfield) in result:
                continue
            if not isinstance(subfield, Compound):
                if is_pure_primitive_field(subfield) and not is_primitive_field(subfield):
                    continue
            compounds.append(type(subfield))
    return result
