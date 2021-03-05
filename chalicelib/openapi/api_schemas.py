from marshmallow import Schema, fields


#
# from chalicelib.openapi.schemas import DeletionSchema, RequestControlSchema, MetaSchema, LinkSchema
#

class UploadResponseSchema(Schema):
    message = fields.Str(example="Upload success")


class UploadErrorResponseSchema(Schema):
    message = fields.Str(example="Upload failed")
