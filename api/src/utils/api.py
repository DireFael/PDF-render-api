from flask import make_response, jsonify
from marshmallow import ValidationError

from src.utils.exceptions import ErrorException, InvalidArgumentsException


def make_validation_error_message(errors, args, prefix=""):

    def _get_error_code(field):

        error_code = "not_valid"

        if field != "_schema" and not isinstance(field, int):

            params = args.copy()

            if prefix:
                keys = prefix.split(".")

                for key in keys:

                    try:
                        key = int(key)
                        params = params[key]
                    except:
                        params = params.get(key, {})

            if field not in params:
                error_code = "required"

        return error_code
    
    def _get_field_name(field):

        if prefix and field == "_schema":
            return prefix

        if field and not prefix:
            return f"{field}"

    
    results = []

    for field, errors in errors.items():
        if isinstance(errors, list):
            for error in errors:
                if isinstance(error, str):
                    
                    results.append({
                        "error_code": _get_error_code(field),
                        "error_message": error,
                        "fields": [_get_field_name(field)]
                    })
                elif isinstance(error, dict):

                    error["fields"] = [_get_field_name(field)] if "fields" not in error else error["fields"]
                    results.append(error)
        elif isinstance(errors, dict):
            results += make_validation_error_message(errors, args, _get_field_name(field))

    return results

def sub_invalid_chars_str(data):
    return str(data).encode("iso8859_2", "ignore").decode("iso8859_2").strip()

def remove_invalid_chars(data):

    if isinstance(data, dict):

        for key, value in data.items():
            data[key] = remove_invalid_chars(value)

    elif type(data) in (list, tuple):
    
        data = list(data)

        for i, value in enumerate(data):
            data[i] = remove_invalid_chars(value)

    elif isinstance(data, str):
        data = sub_invalid_chars_str(data)

    return data

def validate(schema, parameters, context=None, partial=False):
# Validate data by schema

    parameters = remove_invalid_chars(parameters)

    validate_data = {}
    errors = {}

    try:
        validate_data = schema(context=context, partial=partial).load(parameters, partial=partial)
    except ValidationError as err:
        errors = err.messages
    
    if errors:
        raise InvalidArgumentsException(data={"errors": make_validation_error_message(errors, parameters)})

    return validate_data

def serialize(schema, data, only=None, exclude=None, context=None):
# Serializing data by schema 

    many = isinstance(data, list)

    serialize_data = {}
    errors = {}

    try:
        serialize_data = schema(many=many, only=only, exclude=exclude if exclude else [], context=context).dump(data)
    except ValidationError as err:
        errors = err.messages

    if errors:
        raise ErrorException("Invalid data", data=errors)

    return serialize_data

def ok(status_code=200, message='OK', data=None, add_status=True):
# Make custom OK response

    response = data if data else {}

    if add_status:

        response["status_code"] = status_code
        response["status_message"] = message

    return make_response(jsonify(response), status_code)