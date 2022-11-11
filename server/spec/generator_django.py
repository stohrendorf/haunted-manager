import humps
from endpoints import Endpoint, HttpMethod
from structural import (
    ArrayField,
    BaseField,
    BooleanField,
    Compound,
    FloatField,
    IntegerField,
    StringField,
    is_primitive_field,
    is_pure_primitive_field,
)


def _field_to_type_sig(field: BaseField) -> str:
    if isinstance(field, StringField):
        t = "str"
    elif isinstance(field, IntegerField):
        t = "int"
    elif isinstance(field, FloatField):
        t = "float"
    elif isinstance(field, BooleanField):
        t = "bool"
    elif isinstance(field, ArrayField):
        t = f"List[{_field_to_type_sig(field.items)}]"
    else:
        t = f'"{field.typename()}"'

    return f"Optional[{t}]" if field.nullable else t


base_indent = " " * 4


def _gen_check(context: str, indent: str, field: BaseField, accessor: str) -> tuple[str, bool]:
    output = ""
    empty = True

    if not field.nullable:
        output += f'{indent}if {accessor} is None: raise SchemaValidationError("{context}")\n'
    else:
        output += f"{indent}if {accessor} is not None:\n"
        indent += base_indent

    if isinstance(field, StringField):
        if field.min_length is not None:
            output += f'{indent}if len({accessor}) < {field.min_length}: raise SchemaValidationError("{context}")\n'
            empty = False
        if field.max_length is not None:
            output += f'{indent}if len({accessor}) > {field.max_length}: raise SchemaValidationError("{context}")\n'
            empty = False
        if field.regex is not None:
            output += (
                f'{indent}if not re.fullmatch(r"{field.regex}", {accessor}): raise SchemaValidationError("{context}")\n'
            )
            empty = False
    elif isinstance(field, (IntegerField, FloatField)):
        if field.min is not None:
            output += f'{indent}if {accessor} < {field.min}: raise SchemaValidationError("{context}")\n'
            empty = False
        if field.max is not None:
            output += f'{indent}if {accessor} > {field.max}: raise SchemaValidationError("{context}")\n'
            empty = False
    elif isinstance(field, ArrayField):
        output += f"{indent}for field_data in {accessor}:\n"
        if isinstance(field.items, Compound):
            output += f"{indent}    validate_{humps.decamelize(field.items.typename())}(field_data)\n"
            empty = False
        else:
            field_output, empty = _gen_check(context, indent + base_indent, field.items, "field_data")
            output += field_output
        if empty:
            output += f"{indent}    pass\n"
        empty = False

    if field.nullable and empty:
        output += f"{indent}pass\n"

    return output, empty


def _gen_django_field_checks(context: str, accessor: str, field: BaseField) -> str:
    output, _ = _gen_check(context, base_indent, field, accessor)
    return output


def gen_django(schemas: list[BaseField | Compound], endpoints: dict[str, dict[HttpMethod, Endpoint]]) -> str:
    output = "from typing import Callable, Optional, List\n"
    output += "from dataclasses import dataclass\n"
    output += "from dataclasses_json import DataClassJsonMixin, dataclass_json\n"
    output += "from django.http import HttpRequest, HttpResponse\n"
    output += "from django.urls import path\n"
    output += "from . import json_response\n"
    output += "import re\n"
    output += "class SchemaValidationError(Exception):\n"
    output += "    def __init__(self, path: str):\n"
    output += "        super().__init__(path)\n"
    output += "        self.path = path\n"

    output += "    def __str__(self):\n"
    output += '        return f"Schema validation error at {self.path}"\n'

    for schema in schemas:
        if not is_primitive_field(schema):
            output += "@dataclass_json\n"
            output += "@dataclass(kw_only=True)\n"
            output += f"class {schema.typename()}(DataClassJsonMixin):\n"
            for field_name, field in schema.subfields():
                output += f"    {field_name}: {_field_to_type_sig(field)}\n"

            output += "    def validate(self):\n"
            output += f"        validate_{humps.decamelize(schema.typename())}(self)\n"

            output += "\n"

    for schema in schemas:
        if not is_primitive_field(schema):
            output += f"def validate_{humps.decamelize(schema.typename())}(data: {schema.typename()}):\n"
            for field_name, field in schema.subfields():
                output += _gen_django_field_checks(
                    f"{schema.typename()}.{field_name}",
                    f"data.{field_name}",
                    field,
                )
            output += "    return\n"
        elif not is_pure_primitive_field(schema):
            output += (
                f"def validate_{humps.decamelize(schema.typename())}(data: Optional[{_field_to_type_sig(schema)}]):\n"
            )
            output += _gen_django_field_checks(schema.typename(), "data", schema)
            output += "    return\n"

    for path, methods_endpoints in endpoints.items():
        for method, endpoint in methods_endpoints.items():
            output += f"class {humps.decamelize(endpoint.operation_name)}:\n"
            output += f'    path = "{path.lstrip("/")}"\n'
            output += f'    operation = "{humps.decamelize(endpoint.operation_name)}"\n'
            output += "    @classmethod\n"
            if method == HttpMethod.POST:
                assert endpoint.body is not None
                output += (
                    f"    def wrap(cls, fn: Callable[[HttpRequest, {endpoint.body.typename()}],"
                    f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]):\n"
                )
            elif method in (HttpMethod.GET, HttpMethod.DELETE):
                output += (
                    f"    def wrap(cls, fn: Callable[[HttpRequest],"
                    f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]):\n"
                )
            else:
                raise RuntimeError
            output += "        @json_response\n"
            output += (
                f"        def request_handler(request: HttpRequest)"
                f" -> tuple[int, {endpoint.response.typename()}] | {endpoint.response.typename()}:\n"
            )
            if method == HttpMethod.POST:
                assert endpoint.body is not None
                output += (
                    f"            rq: {endpoint.body.typename()} = {endpoint.body.typename()}"
                    f".schema().loads(request.body.decode())\n"
                )
                output += "            rq.validate()\n"
                output += "            response = fn(request, rq)\n"
            elif method in (HttpMethod.GET, HttpMethod.DELETE):
                output += "            response = fn(request)\n"
            else:
                raise RuntimeError

            output += "            if isinstance(response, tuple):\n"
            output += "                code, response = response\n"
            output += "            else:\n"
            output += "                code = HttpResponse.status_code\n"
            output += "            response.validate()\n"
            output += "            return code, response\n"
            output += "        return path(cls.path, request_handler, name=cls.operation)\n"

    return output
