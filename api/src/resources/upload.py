import os

from flask import Blueprint, request

from src.utils.api import ok
from src.utils.exceptions import InvalidArgumentsException
from src.utils.utils import save_document_to_db
from src.utils.worker import render_pdf

upload = Blueprint('upload', __name__)

# Possible to change - define in config to better operating with
ALLOWED_MIME_TYPE = 'application/pdf'
PDF_PATH = os.path.join(os.path.abspath(os.getcwd()),"data", "pdf")

def _save_pdf_to_local(data, src_name):
    pdf_path = os.path.join(PDF_PATH, src_name)

    with open(pdf_path, "wb") as pdf_handler:
        pdf_handler.write(data.read())

@upload.route('/upload', methods=['POST'])
def upload_pdf():
# Check if data in request contain file data with proper MIME type. Get name of file and save to local disk
    if 'file' in request.files:

        # Possible to change - may accept more than one file
        if len(request.files.getlist("file")) != 1:
            raise InvalidArgumentsException("expected_just_one_file", "Expected just one file")

        if request.files["file"].mimetype != ALLOWED_MIME_TYPE:
            raise InvalidArgumentsException("bad_type", f"Unsupported file type. Supported file type {ALLOWED_MIME_TYPE}")

        file_stream =  request.files["file"].stream
        file_name = request.files["file"].filename.split('\\')[-1]

        document_id = save_document_to_db(name=file_name)
        src_name = f"{document_id}-{file_name}"
        
        _save_pdf_to_local(file_stream, src_name)
        # send message to broker for asynchronous processing
        render_pdf.send(file_name, document_id, src_name)

    else:
        InvalidArgumentsException("no_file_provided", "No file provided")    

    return ok(status_code=201, data={"document_id": document_id})
