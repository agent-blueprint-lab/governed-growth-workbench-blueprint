from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import FormatChecker
from jsonschema.validators import validator_for

from .io import load_json


class ValidationError(ValueError):
    """Raised when an input does not satisfy its public contract."""


def validate_instance(instance: Any, schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if not errors:
        return

    rendered = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        rendered.append(f"{label}.{location}: {error.message}")
    raise ValidationError("\n".join(rendered))


def validate_many(items: list[dict[str, Any]], schema_path: Path, label: str) -> None:
    for index, item in enumerate(items):
        validate_instance(item, schema_path, f"{label}[{index}]")
