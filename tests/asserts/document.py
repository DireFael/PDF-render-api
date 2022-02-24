#!/usr/bin/env python
# -*- coding: utf-8 -*-

from asserts.base import (
    assert_base_response, assert_base_response_structure_data, assert_base_error_message, assert_base_response_list_data, assert_base_type_data)

DOCUMENT_BASE = {
    "id": int,
    "name": str,
    "status": int,
    "page_count": int
}

DOCUMENT_WITH_IMG = {
    "id": int,
    "name": str,
    "status": int,
    "page_count": int,
    "images": list
}

IMAGES = {
    "images": list
}

IMAGE_BASE = {
    "id": int,
    "position": int,
    "src": str
}

UPLOAD_BASE =  int


def valid_document_response(result):

    assert_base_response(result, expected_status_code=200, expected_status_message="OK", expected_item_in_dict="data")
    assert_base_response_structure_data(result["data"], DOCUMENT_BASE)

def valid_processed_document_response(result):

    assert_base_response(result, expected_status_code=200, expected_status_message="OK", expected_item_in_dict="data")
    assert_base_response_structure_data(result["data"], DOCUMENT_WITH_IMG)
    assert_base_response_list_data(result["data"]["images"], IMAGE_BASE)

def not_found_response(result):

    assert_base_response(result, expected_status_code=404, expected_status_message="Not found")

def invalid_argument_response(result):

    assert_base_response(result, expected_status_code=422, expected_status_message="Invalid arguments", expected_item_in_dict="description")
    assert_base_error_message(result["description"]["errors"])

def valid_images_response(result):

    assert_base_response(result, expected_status_code=200, expected_status_message="OK", expected_item_in_dict="data")
    assert_base_response_structure_data(result["data"], IMAGES)
    assert_base_response_list_data(result["data"]["images"], IMAGE_BASE)

def valid_image_response(result):

    assert_base_response(result, expected_status_code=200, expected_status_message="OK")

def valid_upload_response(result):

    assert_base_response(result, expected_status_code=201, expected_status_message="OK",)
    assert_base_type_data(result["document_id"], UPLOAD_BASE)

def internal_server_error_response(result):

    assert_base_response(result, expected_status_code=500, expected_status_message="Internal server error")
