from pathlib import Path
from typing import Iterable

from endpoints import Endpoint
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


def _gen_vue_field_checks(context: str, accessor: str, field: BaseField) -> Iterable[str]:
    yield f'  if({accessor} === undefined) throw new SchemaValidationError("{context}");'
    if not field.nullable:
        yield f'  if({accessor} === null) throw new SchemaValidationError("{context}");'
    else:
        yield f"  if({accessor} !== null) {{"

    if isinstance(field, StringField):
        if field.min_length is not None:
            yield f'  if({accessor}.length < {field.min_length}) throw new SchemaValidationError("{context}");'
        if field.max_length is not None:
            yield f'  if({accessor}.length > {field.max_length}) throw new SchemaValidationError("{context}");'
        if field.regex is not None:
            yield f'  if(!{accessor}.match(/^{field.regex}$/)) throw new SchemaValidationError("{context}");'
    elif isinstance(field, (IntegerField, FloatField)):
        if field.min is not None:
            yield f'  if({accessor} < {field.min}) throw new SchemaValidationError("{context}");'
        if field.max is not None:
            yield f'  if({accessor} > {field.max}) throw new SchemaValidationError("{context}");'
    elif isinstance(field, ArrayField):
        yield f"  for ( const fieldData of {accessor} ) {{\n"
        if isinstance(field.items, Compound):
            yield f"      validate{field.items.typename()}(fieldData);\n"
        else:
            yield from _gen_vue_field_checks(context, "fieldData", field.items)
        yield "}\n"

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


def gen_vue(schemas: list[BaseField | Compound], endpoints: list[Endpoint]) -> str:
    output = "/* eslint-disable no-empty */\n"
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

    for endpoint in endpoints:
        output += f"export async function { endpoint.operation_name }("
        if endpoint.body is not None:
            output += f"body: I{endpoint.body.typename()}"
        output += f"): Promise<I{endpoint.response.typename()}> {{\n"
        if endpoint.body is not None:
            output += f"  validate{ endpoint.body.typename() }(body);\n"
        output += f'  const result = (await { endpoint.method }("{ endpoint.path }"'
        if endpoint.body is not None:
            output += ", body"
        output += f")) as I{endpoint.response.typename()};\n"
        output += f"  validate{ endpoint.response.typename() }(result);\n"
        output += "  return result;\n"
        output += "}\n"

    output += (Path(__file__).parent / "data" / "vue_django_common.ts").read_text()

    return output
