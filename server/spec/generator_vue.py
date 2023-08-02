from pathlib import Path
from typing import Iterable

import humps
from endpoints import ApiPath, Endpoint, HttpMethod, get_url_params
from structural import (
    ArrayField,
    BaseField,
    BooleanField,
    Compound,
    FileResponse,
    FilesBody,
    FloatField,
    IntegerField,
    StringField,
    is_primitive_field,
    is_pure_primitive_field,
)


def _gen_vue_field_checks(context: str, accessor: str, field: BaseField) -> Iterable[str]:
    yield f'  if({accessor} === undefined) throw new SchemaValidationError("{context} is undefined");'
    if not field.nullable:
        yield f'  if({accessor} === null) throw new SchemaValidationError("{context} is null");'
    else:
        yield f"  if({accessor} !== null) {{"

    if isinstance(field, StringField):
        if field.min_length is not None:
            yield f"  if({accessor}.length < {field.min_length})"
            yield f'    throw new SchemaValidationError("{context} is too short");'
        if field.max_length is not None:
            yield f"  if({accessor}.length > {field.max_length})"
            yield f'    throw new SchemaValidationError("{context} is too long");'
        if field.regex is not None:
            yield f"  if(!{accessor}.match(/^{field.regex}$/))"
            yield f'    throw new SchemaValidationError("{context} has an invalid format");'
    elif isinstance(field, (IntegerField, FloatField)):
        if field.min is not None:
            yield f"  if({accessor} < {field.min})"
            yield f'    throw new SchemaValidationError("{context} has a value below minimum");'
        if field.max is not None:
            yield f"  if({accessor} > {field.max})"
            yield f'    throw new SchemaValidationError("{context} has a value above maximum");'
    elif isinstance(field, ArrayField):
        yield f"  for( const fieldData of {accessor} ) {{\n"
        if isinstance(field.items, Compound):
            yield f"      validate{field.items.typename()}(fieldData);\n"
        else:
            yield from _gen_vue_field_checks(context, "fieldData", field.items)
        yield "}\n"
    elif isinstance(field, Compound):
        yield f"      validate{field.typename()}({accessor});\n"

    if field.nullable:
        yield "  }"

    yield ""


def _field_to_type_sig(field: BaseField) -> str:
    if isinstance(field, StringField):
        t = "string"
    elif isinstance(field, (IntegerField, FloatField)):
        t = "number"
    elif isinstance(field, BooleanField):
        t = "boolean"
    elif isinstance(field, ArrayField):
        t = f"{_field_to_type_sig(field.items)}[]"
    else:
        t = f"I{field.typename()}"

    return f"{t}|null" if field.nullable else t


def gen_vue(schemas: list[BaseField | Compound], endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]) -> str:
    output = "/* eslint-disable no-empty comma-dangle */\n"
    output += "// noinspection RedundantIfStatementJS\n"

    for schema in schemas:
        if not is_primitive_field(schema):
            output += f"export interface I{schema.typename()} {{\n"
            for field_name, field in schema.subfields():
                output += f"  {field_name}:{_field_to_type_sig(field)};\n"
            output += "}\n"

    for schema in schemas:
        if not is_primitive_field(schema):
            output += f"function validate{schema.typename()}(data: I{schema.typename()}): void {{\n"
            for field_name, field in schema.subfields():
                output += "\n".join(
                    _gen_vue_field_checks(f"{schema.typename()}.{field_name}", f"data.{field_name}", field),
                )
            output += "}\n"
        elif not is_pure_primitive_field(schema):
            output += f"function validate{schema.typename()}(data?: {_field_to_type_sig(schema)}|null): void {{\n"
            output += "\n".join(_gen_vue_field_checks(schema.typename(), "data", schema))
            output += "}\n"

    for path, methods_endpoints in endpoints.items():
        url_params = get_url_params(path.path)

        def convert_type(type: str) -> str:
            return {
                "int": "number",
                "str": "string",
            }[type]

        ts_url = path.path
        for p_name, p_spec in url_params.items():
            ts_url = ts_url.replace(
                f"<{p_spec.type}:{p_name}>",
                f"${{encodeURIComponent({humps.camelize(p_name)})}}",
            )

        args_str = ", ".join(
            (f"{p_name}: {convert_type(p_spec.type)}" for p_name, p_spec in url_params.items()),
        )
        for method, endpoint in methods_endpoints.items():
            output += f"export async function {endpoint.operation_name}("
            if args_str:
                output += args_str
            if endpoint.body is not None:
                if args_str:
                    output += ", "
                if isinstance(endpoint.body, FilesBody):
                    output += "files: File[]"
                else:
                    output += f"body: I{endpoint.body.typename()}"
            result_type = (
                "ReadableStream<Uint8Array> | null"
                if isinstance(endpoint.response, FileResponse)
                else f"I{endpoint.response.typename()}"
            )
            output += f"): Promise<{result_type}> {{\n"
            if endpoint.body is not None and not isinstance(endpoint.body, FilesBody):
                output += f"  validate{endpoint.body.typename()}(body);\n"
            if isinstance(endpoint.body, FilesBody):
                output += f"  const result = (await do{method.value.capitalize()}Files(`{ts_url}`"
            else:
                file_suffix = "File" if isinstance(endpoint.response, FileResponse) else ""
                output += f"  const result = (await do{method.value.capitalize()}{file_suffix}(`{ts_url}`"
            if endpoint.body is not None:
                if isinstance(endpoint.body, FilesBody):
                    output += ", files"
                else:
                    output += ", body"
            output += f")) as {result_type};\n"
            if not isinstance(endpoint.response, FileResponse):
                output += f"  validate{ endpoint.response.typename() }(result);\n"
            output += "  return result;\n"
            output += "}\n"

    output += (Path(__file__).parent / "data" / "vue_django_common.ts").read_text()

    return output
