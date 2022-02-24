import logging
import io
import os

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFPageCountError

from src.models.document import Document
from src.utils.exceptions import UnexpectedErrorException, NotFoundException
from src.utils.utils import save_image_to_db

PDF_DIR_PATH = os.path.join(os.path.abspath(os.getcwd()),"data", "pdf")
IMG_DIR_PATH = os.path.join(os.path.abspath(os.getcwd()), "data", "img")

# Possible to change - define in config to better operating with
#broker = RabbitmqBroker(url="amqp://guest:guest@broker:5672")
broker = RabbitmqBroker(url="amqp://guest:guest@localhost:5672")
dramatiq.set_broker(broker)

# Possible to change - better operation with individual PNG images
@dramatiq.actor
def render_pdf(name, document_id, src_name):
# Function render images from PNG. First change document status, try open PDF from local file.
# Converting PDF bytes to individual PNG files. These are then saved to local and database.
# After render all image, again change document status.


    # Possible to expand - in init using share context
    from app import app

    with app.app_context():
        logging.info(f"Start processing PDF file - {src_name}")

        Document.update_status(document_id, 1)

        pdf_path = os.path.join(PDF_DIR_PATH, src_name)

        if not os.path.isfile(pdf_path):
            Document.update_status(document_id, 2)
            raise NotFoundException(f"Document with name {src_name} not found!")

        try:
            with open(pdf_path, "rb") as pdf_handler:
                pdf_data = pdf_handler.read()
        except Exception as err:
            Document.update_status(document_id, 2)
            raise UnexpectedErrorException(f"Error when trying open pdf({src_name})", {err})

        try:
            pages = convert_from_bytes(pdf_data, dpi=600, fmt="png", size=(1200,1600))
        except PDFPageCountError as e:
            Document.update_status(document_id, 2)
            raise UnexpectedErrorException(f"Converting PDF({name}) error", {e})
        except Exception as err:
            Document.update_status(document_id, 2)
            raise UnexpectedErrorException(f"General PDF({name}) error", {err})

        page_count = len(pages)
        actual_page = 0

        for page in pages:

            actual_page += 1

            logging.info(f"Start processing page {actual_page} from PDF file - {src_name}")
            image_src = f"{document_id}-{actual_page}_{page_count}.png"

            path = os.path.join(IMG_DIR_PATH, image_src)
            byteIO = io.BytesIO()
            page.save(byteIO, format="png")
            image_byte_data = byteIO.getvalue()
            page.save(path, format="png")

            save_image_to_db(image_byte_data, image_src, actual_page, document_id)

        logging.info(f"Finish processing PDF file - {src_name}")
        Document.update_status(document_id, 3, actual_page)
