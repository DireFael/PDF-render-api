#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from utils.client import APIClient

small_pdf_path = os.path.join(os.path.abspath(os.getcwd()),"data", "small.pdf")
large_pdf_path = os.path.join(os.path.abspath(os.getcwd()),"data", "large.pdf")


@pytest.fixture(scope="session")
def processed_document_id():
    
    data = {
        'file': (small_pdf_path, open(small_pdf_path, 'rb'), "application/pdf")
    }

    result = APIClient().post(module=f"/upload", data=data)

    print(result)

    return result["document_id"]

@pytest.fixture(scope="session")
def nonprocessed_document_id():

    data = {
        'file': (large_pdf_path, open(large_pdf_path, 'rb'), "application/pdf")
    }

    result = APIClient().post(module=f"/upload", data=data)

    return result["document_id"]

@pytest.fixture(scope="session")
def proper_upload_data():

    data = {
        'file': (small_pdf_path, open(small_pdf_path, 'rb'), "application/pdf")
    }
    
    return data

@pytest.fixture(scope="session")
def proper_upload_data():

    data = {
        'file': (small_pdf_path, open(small_pdf_path, 'rb'), "application/pdf")
    }
    
    return data

@pytest.fixture(scope="session")
def invalid_mime_upload_data():

    data = {
        'file': (small_pdf_path, open(small_pdf_path, 'rb'), "application/json")
    }
    
    return data
