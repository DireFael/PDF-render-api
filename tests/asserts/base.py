#!/usr/bin/env python
# -*- coding: utf-8 -*-

def assert_base_response(result, expected_status_code, expected_status_message=None, expected_item_in_dict=None):

    assert 'status_code' in result, f"Status code not found in result: {result}."
    assert type(result['status_code']) is int, f"Status code is not a integer. It's {type(result['status_code'])}."
    assert expected_status_code == result['status_code'], f"Expected status code is {expected_status_code} get {result['status_code']}."

    assert 'status_message' in result, f"Status message not found in result: {result}."
    assert type(result['status_message']) is str, f"Status message is not a string. It's {type(result['status_message'])}."

    if expected_status_message:
        assert expected_status_message == result['status_message'], f"Expected status message is {expected_status_message} get {result['status_message']}."

    if expected_item_in_dict:
        assert type(result) is dict, f"Expected result type is dict get {type(result)}."
        assert expected_item_in_dict in result, f"Expected {expected_item_in_dict} in result dict structure, but not found."

def assert_base_error_message(error):

    assert type(error) is dict, f"Errors structure is not a dict. It's {type(error)}"

    assert 'field' in error, f"Expecting field in {error}, but not found."
    assert 'error_message' in error, f"Expecting error_message in {error}, but not found."
    assert 'error_code' in error, f"Expecting error_code in {error}, but not found."

def assert_base_type_data(data, data_type):

    assert type(data) is data_type, f"Expecting {data_type} but data is {type(data)}"

def assert_base_response_structure_data(data, structure):

    for item in structure:
        assert item in data, f"Expecting {item} in {data}, but not found."

        if data[item] is not None:
            assert type(data[item]) is structure[item], f"Expecting {item} with data type {structure[item]}, but get {type(data[item])}."

def assert_base_response_list_data(list_data, structure):

    assert type(list_data) is list, f"Errors structure is not a list. It's {type(list_data)}"

    for item in list_data:
        assert_base_response_structure_data(item, structure)