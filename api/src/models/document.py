from src.extensions import db
from src.schemas.document import DocumentSchema, ListImagesSchema, ListImagesFullSchema, ImageFullSchema
from src.utils.api import serialize
from src.utils.exceptions import NotFoundException


# Possible to expand - make baseModel which have all classmethod(from both Models) or method get to list, deleted or create Model(with try and rollback)
class Document(db.Model):

    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    # Possible to change - use Enum insted of Integer
    status = db.Column(db.Integer, nullable=False)
    page_count = db.Column(db.Integer, nullable=False)

    def __init__(self, name=None, status=0, page_count=0):

        self.name = name
        self.status = status
        self.page_count = page_count

    def __repr__(self):
        return f"<Document {repr(self.id)}>"

    @classmethod
    def update_status(self, document_id, status, page_count=0):
    # Update status document

        doc = self.query.filter_by(id=document_id).first()
        doc.status = status
        doc.page_count = page_count
        db.session.commit()

    @classmethod
    def get_document(self, document_id):
    # Get information about document. If the PDF is rendered, we add information about the rendered images

        doc = self.query.filter_by(id=document_id).first()

        if doc is None:
            raise NotFoundException(f"Data for document with id {document_id} not found!")

        result = serialize(DocumentSchema, doc)

        if result["status"] == 3:
            result.update(Image.get_images(document_id))

        return result

class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    src = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)

    def __init__(self, data, src, position, document_id):
        self.data = data
        self.src = src
        self.position = position
        self.document_id = document_id

    def __repr__(self):
        return f"<Image {repr(self.id)} of document {repr(self.document_id)}>"

    @classmethod
    def get_images(self, document_id):
    # Get images related to document_id, if exist

        images = self.query.filter_by(document_id=document_id).all()

        if images is None:
            return {}

        result = serialize(ListImagesSchema, {"images": images})

        return result

    @classmethod
    def get_full_images(self, document_id):
    # Get full information about images related to document_id, if exist

        images = self.query.filter_by(document_id=document_id).all()

        if images is None:
            raise NotFoundException(f"Images for document with id {document_id} not found!")

        result = serialize(ListImagesFullSchema, {"images": images})

        return result

    @classmethod
    def get_image_data(self, image_id):
    # Get data about image, generate uniq name with actual page(downloaded) and max page in document

        image = self.query.filter_by(id=image_id).first()
        
        if image is None:
            raise NotFoundException(f"Image with id {image_id} not found!")

        image_data = serialize(ImageFullSchema, image)

        doc = Document.query.filter_by(id=image_data["document_id"]).first()

        if doc is None:
            raise NotFoundException(f"Data for document with id {image_data['document_id']} not found!")

        doc_data = serialize(DocumentSchema, doc)
        name = doc_data["name"].split(".")[0]

        return {
            "image_id": image_id,
            "src": image_data["src"],
            "image_name": f"{name}_pdf-page_{image_data['position']}-page_{doc_data['page_count']}.png"
        }
