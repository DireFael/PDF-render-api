#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asserts.document as document
from utils.client import APIClient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Testing /documnent/{id} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def test_get_document(nonprocessed_document_id):

    result = APIClient().get(module=f"/document/{nonprocessed_document_id}")
    print(result)
    document.valid_document_response(result)

def test_get_processed_document(processed_document_id):

    result = APIClient().get(module=f"/document/{processed_document_id}")
    document.valid_processed_document_response(result)

def test_get_nonexist_document(processed_document_id):

    # change id to non-exist
    document_id = processed_document_id + 50

    result = APIClient().get(module=f"/document/{document_id}")
    document.not_found_response(result)

def test_invalid_argument_document():

    result = APIClient().get(module=f"/document/test")
    document.invalid_argument_response(result)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Testing /documnent/{id}/images ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_get_processed_images(processed_document_id):

    result = APIClient().get(module=f"/document/{processed_document_id}/images")
    document.valid_images_response(result)

def test_invalid_argument_document():

    result = APIClient().get(module=f"/document/test/images")
    document.invalid_argument_response(result)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Testing /documnent/image/{id} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_get_processed_image(processed_document_id):

    doc_result = APIClient().get(module=f"/document/{processed_document_id}/images")
    image_id = doc_result["data"]["images"][0]["id"]

    result = APIClient().get_file(module=f"/document/image/{image_id}")
    document.valid_image_response(result)

def test_get_nonexist_processed_image(processed_document_id):

    doc_result = APIClient().get(module=f"/document/{processed_document_id}/images")
    processed_image_id = doc_result["data"]["images"][0]["id"]
    # change id to non-exist
    image_id = processed_image_id + 50

    result = APIClient().get(module=f"/document/image/{image_id}")

    document.not_found_response(result)

def test_invalid_argument_document():

    result = APIClient().get(module=f"/document/image/test")
    document.invalid_argument_response(result)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Testing /upload ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_valid_upload(proper_upload_data):

    result = APIClient().post(module=f"/upload", data=proper_upload_data)
    document.valid_upload_response(result)

def test_invalid_mime_type_file_upload(invalid_mime_upload_data):

    result = APIClient().post(module=f"/upload", data=invalid_mime_upload_data)
    document.invalid_argument_response(result)

