from mongoengine import Document, fields

from category.models import Category
from users.models import User


class Request(Document):
    category_id = fields.StringField(required=True)
    mobile = fields.StringField(max_length=11)
    # todo keep a check
    radius = fields.IntField(required=True)
    location = fields.PointField(required=True)
    comment = fields.StringField(max_length=1000)
    created_at = fields.DateTimeField(required=True)
    user_id = fields.StringField(max_length=300)
    isCompleted = fields.BooleanField(default=False)
    isPaid = fields.BooleanField(default=False)
    isExpired = fields.BooleanField(default=False)
    provider_id = fields.StringField(max_length=300)

    meta = {"db_alias": "default"}
