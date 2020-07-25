from mongoengine import Document, fields

from category.models import Category
from users.models import User


class Request(Document):
    category_id = fields.IntField(required=True)
    title = fields.StringField(max_length=300)
    mobile = fields.StringField(max_length=11)
    # todo keep a check
    location = fields.PointField(required=True)
    comments = fields.StringField(max_length=1000)
    creation_date = fields.DateTimeField(required=True)
    user_id = fields.StringField(max_length=300)
    isCompleted = fields.BooleanField(default=False)
    isPaid = fields.BooleanField(default=False)
    isClosed = fields.BooleanField(default=False)
    provider_id = fields.StringField(max_length=300)
    complaints = fields.ListField(fields.StringField())

    meta = {"db_alias": "default"}


