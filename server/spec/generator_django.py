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
        t = field.typename()

    return f"Optional[{t}]" if field.nullable else t


base_indent = " " * 4


def _gen_check(context: str, indent: str, field: BaseField, accessor: str) -> tuple[str, bool]:
    output = ""
    empty = True

    if not field.nullable:
        output += f'{indent}if {accessor} is None: raise SchemaValidationError("{context} is null")\n'
    else:
        output += f"{indent}if {accessor} is not None:\n"
        indent += base_indent

    if isinstance(field, StringField):
        if field.min_length is not None:
            output += f"{indent}if len({accessor}) < {field.min_length}:\n"
            output += f'{indent + base_indent}raise SchemaValidationError("{context} is too short")\n'
            empty = False
        if field.max_length is not None:
            output += f"{indent}if len({accessor}) > {field.max_length}:\n"
            output += f'{indent + base_indent}raise SchemaValidationError("{context} is too long")\n'
            empty = False
        if field.regex is not None:
            output += f'{indent}if not re.fullmatch(r"{field.regex}", {accessor}):\n'
            output += f'{indent + base_indent}raise SchemaValidationError("{context} has an invalid format")\n'
            empty = False
    elif isinstance(field, (IntegerField, FloatField)):
        if field.min is not None:
            output += f"{indent}if {accessor} < {field.min}:\n"
            output += f'{indent + base_indent}raise SchemaValidationError("{context} has a value below minimum")\n'
            empty = False
        if field.max is not None:
            output += f"{indent}if {accessor} > {field.max}:\n"
            output += f'{indent+base_indent}raise SchemaValidationError("{context} has a value above maximum")\n'
            empty = False
    elif isinstance(field, ArrayField):
        varname = re.sub(r"[^a-zA-Z0-9]", "_", accessor) + "_entry"
        output += f"{indent}for {varname} in {accessor}:\n"
        if isinstance(field.items, Compound):
            output += f"{indent}    {varname}.validate()\n"
            empty = False
        else:
            field_output, empty = _gen_check(context, indent + base_indent, field.items, varname)
            output += field_output
        if empty:
            output += f"{indent}    pass\n"
        empty = False
    elif isinstance(field, Compound):
        output += f"{indent}{accessor}.validate()\n"
        empty = False

    if field.nullable and empty:
        output += f"{indent}pass\n"

    return output, empty


def _gen_django_field_checks(context: str, accessor: str, field: BaseField, additional_indent_level: int = 0) -> str:
    output, _ = _gen_check(context, base_indent * (additional_indent_level + 1), field, accessor)
    return output


def gen_django(
    schemas: list[BaseField | Compound],
    endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]],
) -> tuple[str, dict[str, str]]:
    schema_outputs = {}
    for schema in schemas:
        if is_primitive_field(schema):
            continue

        dependencies = set(field.typename() for _, field in schema.subfields() if isinstance(field, Compound)) | set(
            field.items.typename()
            for _, field in schema.subfields()
            if isinstance(field, ArrayField) and isinstance(field.items, Compound)
        )

        schema_output = "import re\n"
        schema_output += "from dataclasses_json import DataClassJsonMixin, dataclass_json\n"
        schema_output += "from dataclasses import dataclass\n"
        schema_output += "from typing import List, Optional\n"
        for dependency in dependencies:
            schema_output += f"from .{dependency} import {dependency}\n"
        schema_output += "from ..json_response import Validatable\n"
        schema_output += "from ..error import SchemaValidationError\n"

        schema_output += "\n"

        schema_output += "@dataclass_json\n"
        schema_output += "@dataclass(kw_only=True)\n"
        schema_output += f"class {schema.typename()}(DataClassJsonMixin, Validatable):\n"
        for field_name, field in schema.subfields():
            schema_output += f"    {field_name}: {_field_to_type_sig(field)}\n"

        schema_output += "    def validate(self):\n"
        for field_name, field in schema.subfields():
            schema_output += _gen_django_field_checks(
                f"{schema.typename()}.{field_name}",
                f"self.{field_name}",
                field,
                additional_indent_level=1,
            )
        schema_output += "        return\n"

        schema_outputs[schema.typename()] = schema_output

    output = "from typing import Callable, Optional, List\n"
    output += "from dataclasses import dataclass\n"
    output += "from dataclasses_json import DataClassJsonMixin, dataclass_json\n"
    output += "from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse\n"
    output += "from django.urls import path\n"
    output += "from enum import Enum\n"
    output += "from http import HTTPStatus\n"
    output += "from .json_response import json_response, Validatable\n"
    output += "from .error import SchemaValidationError\n"

    for schema_name in schema_outputs.keys():
        output += f"from .schemas.{schema_name} import {schema_name}\n"

    output += "import re\n"
    output += "import logging\n"
    output += "class HttpMethod(Enum):\n"
    for method in HttpMethod:
        output += f'    {method.name} = "{method.value}"\n'

    for schema in schemas:
        if not is_primitive_field(schema):
            pass
        elif not is_pure_primitive_field(schema):
            output += (
                f"def validate_{humps.decamelize(schema.typename())}(data: Optional[{_field_to_type_sig(schema)}]):\n"
            )
            output += _gen_django_field_checks(schema.typename(), "data", schema)
            output += "    return\n"

    for path, methods_endpoints in endpoints.items():
        url_params = get_url_params(path.path)
        url_arg_types = [p_spec.type for p_spec in url_params.values()]
        url_args_in = [f"{humps.decamelize(p_name)}: {p_spec.type}" for p_name, p_spec in url_params.items()]
        url_args_out = [humps.decamelize(p_name) for p_name in url_params.keys()]
        django_path = path.path
        for p_name, p_spec in url_params.items():
            django_path = django_path.replace(
                f"<{p_spec.type}:{p_name}>",
                f"<{p_spec.type}:{humps.decamelize(p_name)}>",
            )

        output += f"class {humps.decamelize(path.name)}:\n"
        output += f'    path = "{django_path.lstrip("/")}"\n'
        output += f'    name = "{path.name}"\n'
        output += "    @classmethod\n"
        output += "    def wrap(\n"
        output += "        cls,\n"
        output += "        *,\n"
        for method, endpoint in methods_endpoints.items():
            handler_signature = make_handler_signature(url_arg_types, endpoint, method)
            output += f"        {method.name.lower()}_handler: {handler_signature},\n"
        output += "    ):\n"
        output += "        def dispatch(" + ", ".join(["request: HttpRequest"] + url_args_in) + ") -> JsonResponse:\n"
        for method, endpoint in methods_endpoints.items():
            output += f'            if request.method == "{method.value}":\n'
            output += (
                f"                return cls.do_{method.value.lower()}("
                + ", ".join(["request", f"{method.value.lower()}_handler", *url_args_out])
                + ")\n"
            )
        output += "            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)\n"
        output += "        return path(cls.path, dispatch, name=cls.name)\n"

        for method, endpoint in methods_endpoints.items():
            output += "    @json_response\n"
            output += "    @staticmethod\n"
            handler_signature = make_handler_signature(url_arg_types, endpoint, method)
            output += (
                f"    def do_{method.value.lower()}("
                + ", ".join(["request: HttpRequest", f"handler: {handler_signature}", *url_args_in])
                + f") -> {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}] | JsonResponse:\n"
            )
            if method == HttpMethod.POST:
                assert endpoint.body is not None
                output += (
                    f"        body: {endpoint.body.typename()} = {endpoint.body.typename()}"
                    f".schema().loads(request.body.decode())\n"
                )
                output += "        try:\n"
                output += "            body.validate()\n"
                output += "        except SchemaValidationError as e:\n"
                output += '            logging.error("request validation failed", exc_info=True)\n'
                output += '            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})\n'
                output += "        response = handler(" + ", ".join(["request", *url_args_out, "body"]) + ")\n"
            elif method in (HttpMethod.GET, HttpMethod.DELETE):
                output += "        response = handler(" + ", ".join(["request", *url_args_out]) + ")\n"
            else:
                raise RuntimeError

            output += "        if isinstance(response, tuple):\n"
            output += "            code, response = response\n"
            output += "        else:\n"
            output += "            code = HttpResponse.status_code\n"
            output += "        return code, response\n"

    return output, schema_outputs


def make_handler_signature(arg_types: list[str], endpoint: Endpoint, method: HttpMethod) -> str:
    input_signature = ", ".join(["HttpRequest"] + arg_types)

    if method == HttpMethod.POST:
        assert endpoint.body is not None
        handler_signature = (
            f"Callable[[{input_signature}, {endpoint.body.typename()}],"
            f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]"
        )
    elif method in (HttpMethod.GET, HttpMethod.DELETE):
        handler_signature = (
            f"Callable[[{input_signature}],"
            f" {endpoint.response.typename()} | tuple[int, {endpoint.response.typename()}]]"
        )
    else:
        raise RuntimeError
    return handler_signature
