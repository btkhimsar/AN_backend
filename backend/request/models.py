from mongoengine import Document, fields, EmbeddedDocument


class Request(Document):
    category_id = fields.StringField(required=True, max_length=100)
    super_category_id = fields.StringField(required=True, max_length=100)
    mobile = fields.StringField(max_length=11, required=True)
    location = fields.PointField(required=True)
    location_name = fields.StringField(required=True, max_length=100)
    comment = fields.StringField(max_length=1000, required=False, default="")
    created_at = fields.LongField(timestamps=True)
    user_id = fields.StringField(max_length=100, required=True)
    isCompleted = fields.BooleanField(default=False, required=False)
    isExpired = fields.BooleanField(default=False, required=False)
    questions = fields.ListField(fields.DictField())

    meta = {"db_alias": "default"}
