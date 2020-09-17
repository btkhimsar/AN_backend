from mongoengine import Document, fields, EmbeddedDocument


class Request(Document):
    _id = fields.LongField()
    category_id = fields.StringField(required=True, max_length=100)
    super_category_id = fields.StringField(required=True, max_length=100)
    mobile = fields.StringField(max_length=11, required=True)
    location = fields.PointField(required=True)
    location_name = fields.StringField(required=True, max_length=100)
    comment = fields.StringField(max_length=1000, required=False, default="")
    created_at = fields.LongField(timestamps=True)
    user_id = fields.LongField(required=True)
    isCompleted = fields.BooleanField(default=False, required=False)
    questions = fields.ListField(fields.DictField())
    interested_users = fields.ListField(fields.LongField())
    aud_url = fields.StringField(required=False, max_length=50)
    provider_id = fields.LongField()

    meta = {"db_alias": "default"}
