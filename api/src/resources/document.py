from flask import Blueprint, Response

from src.models.document import Document, Image 
from src.utils.api import ok
from src.utils.exceptions import InvalidArgumentsException
from src.utils.utils import open_image

document = Blueprint('document', __name__)

#Possible to change - make valiadion using schema
def _validate_id(parameter_id, source):

    if not parameter_id.isdecimal():
        raise InvalidArgumentsException("id_is_not_number", f"Parameter {source} is not a number")
    
    return int(parameter_id)


@document.route("/document/<document_id>", methods=['GET'])
def get_document(document_id):

    data = Document.get_document(_validate_id(document_id, "document_id"))
    return ok(data={'data': data})

@document.route("/document/<document_id>/images", methods=['GET'])
def get_document_images(document_id):

    data = Image.get_full_images(_validate_id(document_id, "document_id"))
    return ok(data={'data': data})

@document.route("/document/image/<image_id>", methods=['GET'])
def get_image(image_id):
    
    data = Image.get_image_data(_validate_id(image_id, "image_id"))

    image_data = open_image(data["src"])

    headers = {
        "Content-Type": "image/png",
        "Content-Disposition": f"attachment; filename={data['image_name']}"
    }

    return Response(image_data, 200, headers)
