from mongoengine import Document, fields, EmbeddedDocument


class Request(Document):
    _id = fields.LongField()
    category_id = fields.IntField(required=True)
    location = fields.PointField(required=True)
    location_name = fields.StringField(required=True, max_length=100)
    comment = fields.StringField(max_length=100, required=False)
    created_at = fields.LongField(timestamps=True)
    user_id = fields.LongField(required=True)
    is_completed = fields.BooleanField(default=False, required=False)
    questions = fields.DictField(required=False)
    new_interest_count = fields.IntField(required=False, default=0)
    interested_users = fields.ListField(fields.LongField(), required=False)
    aud_url = fields.StringField(required=False, max_length=100)
    completed_by = fields.LongField(required=False)
    share_mobile = fields.BooleanField(required=False, default=False)
    complaints_count = fields.IntField(required=False, default=0)

    meta = {"db_alias": "default"}
