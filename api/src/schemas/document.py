from marshmallow import Schema, fields


class ImageSchema(Schema):
    id = fields.Int(required=True)
    src = fields.String(required=True)
    position = fields.Int(required=True)

class ImageFullSchema(ImageSchema):
    document_id = fields.Int(required=True)

class ListImagesFullSchema(Schema):
    images = fields.List(fields.Nested(ImageFullSchema))

class ListImagesSchema(Schema):
    images = fields.List(fields.Nested(ImageSchema))

class DocumentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    status = fields.Int(required=True)
    page_count = fields.Int(required=True)
