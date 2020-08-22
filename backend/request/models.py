from mongoengine import Document, fields, EmbeddedDocument

class Question(EmbeddedDocument):
    qId = fields.IntField()
    aId = fields.ListField(fields.IntField())
    remarks = fields.StringField(max_length=100, default="")

class Request(Document):
    category_id = fields.StringField(required=True, max_length=50)
    super_category_id = fields.StringField(required=True, max_length=50)
    mobile = fields.StringField(max_length=11)
    # todo keep a check
    location = fields.PointField(required=True)
    location_name = fields.StringField(required=True, max_length=100)
    comment = fields.StringField(max_length=1000)
    created_at = fields.LongField(timestamps=True)
    user_id = fields.StringField(max_length=300)
    isCompleted = fields.BooleanField(default=False)
    isPaid = fields.BooleanField(default=False)
    isExpired = fields.BooleanField(default=False)
    provider_id = fields.StringField(max_length=300)
    complaints = fields.ListField(fields.StringField())
    questions = fields.EmbeddedDocumentListField(Question)

    meta = {"db_alias": "default"}
