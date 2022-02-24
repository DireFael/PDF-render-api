import logging
import os

from src.models.document import db, Document, Image
from src.utils.exceptions import NotFoundException

IMG_PATH = os.path.join(os.path.abspath(os.getcwd()), "data", "img")

def open_image(image_name):
# Possible to expand - If can't open image from local disk, may use data from database

    image_path = os.path.join(IMG_PATH, image_name)

    if not os.path.isfile(image_path):
        raise NotFoundException(f"Image with name {image_name} not found!")

    with open(image_path, "rb") as image_handler:
        image_data = image_handler.read()

    return image_data

def save_document_to_db(name="Undefined", status=0, page_count=0):
# Possible to expand - Do in baseModel in models

    logging.info(f"Saving document {name} with status {status} and page_count{page_count} to database")
    
    doc = Document(name, status, page_count)
    db.session.add(doc)
    db.session.commit()

    return doc.id

def save_image_to_db(data, image_src, position, document_id):
# Possible to expand - Do in baseModel in models

    logging.info(f"Saving image {image_src} with position {position} and document_id {document_id} to database")

    img = Image(data, image_src, position, document_id)
    db.session.add(img)
    db.session.commit()