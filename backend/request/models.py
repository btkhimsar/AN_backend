from mongoengine import Document, fields, EmbeddedDocument


class Request(Document):
    category_id = fields.StringField(max_length=50, required=True)
    location = fields.PointField(required=True)
    location_name = fields.StringField(required=True, max_length=100)
    comment = fields.StringField(max_length=100, required=False)
    user_id = fields.StringField(max_length=50, required=True)
    is_completed = fields.BooleanField(default=False, required=False)
    questions = fields.DictField(required=False)
    new_interest_count = fields.IntField(required=False, default=0)
    interested_users = fields.ListField(fields.StringField(max_length=50), required=False)
    aud_url = fields.StringField(required=False, max_length=100)
    completed_by = fields.StringField(max_length=50, required=False)
    share_mobile = fields.BooleanField(required=True, default=False)
    complaints_count = fields.IntField(required=False, default=0)

    meta = {"db_alias": "default"}
