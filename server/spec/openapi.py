import json

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
)


def _make_openapi_path(path: ApiPath) -> str:
    result = path.path
    url_params = get_url_params(path.path)
    for p_name, p_spec in url_params.items():
        result = result.replace(
            f"<{p_spec.type}:{p_name}>",
            f"{{{humps.camelize(p_name)}}}",
        )
    return result


def _get_type_of(field: BaseField | Compound) -> dict:
    if isinstance(field, IntegerField):
        return {
            "type": "integer",
            "format": "int64",
            **(
                {
                    "minimum": field.min,
                }
                if field.has_min
                else {}
            ),
            **(
                {
                    "maximum": field.max,
                }
                if field.has_max
                else {}
            ),
        }
    elif isinstance(field, FloatField):
        return {
            "type": "number",
            "format": "float",
            **(
                {
                    "minimum": field.min,
                }
                if field.has_min
                else {}
            ),
            **(
                {
                    "maximum": field.max,
                }
                if field.has_max
                else {}
            ),
        }
    elif isinstance(field, StringField):
        return {
            "type": "string",
            **(
                {
                    "minLength": field.min_length,
                }
                if field.has_min_length
                else {}
            ),
            **(
                {
                    "maxLength": field.max_length,
                }
                if field.has_max_length
                else {}
            ),
            **(
                {
                    "pattern": field.regex,
                }
                if field.has_regex
                else {}
            ),
        }
    elif isinstance(field, BooleanField):
        return {
            "type": "boolean",
        }
    elif isinstance(field, ArrayField):
        return {
            "type": "array",
            "items": {
                "$ref": f"#/components/schemas/{humps.camelize(field.items.typename())}",
            }
            if isinstance(field.items, Compound)
            else _get_type_of(field.items),
        }
    elif isinstance(field, Compound):
        return {
            "type": "object",
            "$ref": f"#/components/schemas/{humps.camelize(field.typename())}",
        }
    else:
        raise RuntimeError(f"unexpected type {field}")


def gen_openapi(schemas: list[BaseField | Compound], endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]) -> str:
    document = {
        "openapi": "3.0.0",
        "info": {"title": "Haunted API", "version": "0"},
        "paths": {
            _make_openapi_path(path): {
                method.value.lower(): {
                    "parameters": [
                        {
                            "name": p_name,
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": {
                                    "str": "string",
                                    "int": "integer",
                                }[p_spec.type],
                                "format": {
                                    "str": "",
                                    "int": "int64",
                                }[p_spec.type],
                            },
                        }
                        for p_name, p_spec in get_url_params(path.path).items()
                    ],
                    **(
                        {
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": f"#/components/schemas/{humps.camelize(ep.body.typename())}",
                                        },
                                    },
                                },
                            },
                        }
                        if ep.body
                        else {}
                    ),
                    "responses": {
                        "200": {
                            "description": f"{ep.operation_name} response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": f"#/components/schemas/{humps.camelize(ep.response.typename())}",
                                    },
                                },
                            },
                        },
                    },
                }
                for method, ep in methods_endpoints.items()
            }
            for path, methods_endpoints in endpoints.items()
        },
        "components": {
            "schemas": {
                humps.camelize(schema.typename()): {
                    "type": "object",
                    **(
                        {"required": required}
                        if (
                            required := [
                                field_name for (field_name, field_type) in schema.subfields() if not field_type.nullable
                            ]
                        )
                        else {}
                    ),
                    "properties": {
                        field_name: _get_type_of(field_type) for (field_name, field_type) in schema.subfields()
                    },
                }
                for schema in schemas
            },
        },
    }
    return json.dumps(document)
