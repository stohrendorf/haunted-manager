import re

import humps
from endpoints import ApiPath, Endpoint, HttpMethod, get_url_params
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
        varname = re.sub(r"[^a-zA-Z0-9]", "_", accessor) + "_entry"
        output += f"{indent}for {varname} in {accessor}:\n"
        if isinstance(field.items, Compound):
            output += f"{indent}    validate_{humps.decamelize(field.items.typename())}({varname})\n"
            empty = False
        else:
            field_output, empty = _gen_check(context, indent + base_indent, field.items, varname)
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


def gen_django(schemas: list[BaseField | Compound], endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]) -> str:
    output = "from typing import Callable, Optional, List\n"
    output += "from dataclasses import dataclass\n"
    output += "from dataclasses_json import DataClassJsonMixin, dataclass_json\n"
    output += "from django.http import HttpRequest, HttpResponse\n"
    output += "from django.urls import path\n"
    output += "from enum import Enum\n"
    output += "from . import json_response\n"
    output += "import re\n"
    output += "class SchemaValidationError(Exception):\n"
    output += "    def __init__(self, path: str):\n"
    output += "        super().__init__(path)\n"
    output += "        self.path = path\n"

    output += "    def __str__(self):\n"
    output += '        return f"Schema validation error at {self.path}"\n'
    output += "class HttpMethod(Enum):\n"
    for method in HttpMethod:
        output += f'    {method.name} = "{method.value}"\n'

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
        url_params = get_url_params(path.path)
        args_str = ""
        if url_params:
            args_str = ", " + ", ".join(
                (p_spec.type for p_name, p_spec in url_params.items()),
            )

        output += "\n"
        output += f"class {humps.decamelize(path.name)}:\n"
        output += f'    path = "{path.path.lstrip("/")}"\n'
        output += f'    name = "{path.name}"\n'
        output += "    @classmethod\n"
        output += "    def wrap(\n"
        output += "        cls,\n"
        output += "        *,\n"
        for method, endpoint in methods_endpoints.items():
            handler_signature = make_handler_signature(args_str, endpoint, method)
            output += f"        {method.name.lower()}_handler: {handler_signature},\n"
        output += "    ):\n"
        output += "        def dispatch(request: HttpRequest, *args, **kwargs):\n"
        for method, endpoint in methods_endpoints.items():
            output += f'            if request.method == "{method.value}":\n'
            output += f"                return cls.do_{method.value.lower()}(request, {method.value.lower()}_handler, *args, **kwargs)\n"
        output += "            raise RuntimeError\n"
        output += "        return path(cls.path, dispatch, name=cls.name)\n"

        for method, endpoint in methods_endpoints.items():
            kwargs = ", *args, **kwargs" if args_str or method == HttpMethod.POST else ""
            output += "    @json_response\n"
            output += "    @staticmethod\n"
            handler_signature = make_handler_signature(args_str, endpoint, method)
            output += (
                f"    def do_{method.value.lower()}(request: HttpRequest, handler: {handler_signature}{kwargs})"
                f" -> {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]:\n"
            )
            if method == HttpMethod.POST:
                assert endpoint.body is not None
                output += (
                    f"        body: {endpoint.body.typename()} = {endpoint.body.typename()}"
                    f".schema().loads(request.body.decode())\n"
                )
                output += "        body.validate()\n"
                output += f"        response = handler(request{kwargs}, body=body)\n"
            elif method in (HttpMethod.GET, HttpMethod.DELETE):
                output += f"        response = handler(request{kwargs})\n"
            else:
                raise RuntimeError

            output += "        if isinstance(response, tuple):\n"
            output += "            code, response = response\n"
            output += "        else:\n"
            output += "            code = HttpResponse.status_code\n"
            output += "        response.validate()\n"
            output += "        return code, response\n"

    return output


def make_handler_signature(args_str, endpoint, method):
    if method == HttpMethod.POST:
        assert endpoint.body is not None
        handler_signature = (
            f"Callable[[HttpRequest{args_str}, {endpoint.body.typename()}],"
            f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]"
        )
    elif method in (HttpMethod.GET, HttpMethod.DELETE):
        handler_signature = (
            f"Callable[[HttpRequest{args_str}],"
            f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]"
        )
    else:
        raise RuntimeError
    return handler_signature
