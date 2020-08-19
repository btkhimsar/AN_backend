from mongoengine import Document, fields

from Constants.image_urls import HOME_ICON
from Constants.languages import LANGS
from Constants.user_type import USER_TYPE

class User(Document):
    mobile = fields.StringField(max_length=10, required=True)
    name = fields.StringField(max_length=30, default="")
    user_type = fields.StringField(choices=USER_TYPE, default="consumer", required=False)
    user_language = fields.StringField(choices=LANGS, required=True, default='english')
    expiry = fields.DateTimeField()
    email = fields.StringField(default="", required=False)
    address = fields.StringField(max_length=300, default="")
    profile_image = fields.URLField(default=HOME_ICON)
    work_category = fields.StringField(min_value=1, max_length=100, required=False)
    base_location = fields.PointField(required=False)
    work_radius = fields.IntField(min_value=3, max_value=10, required=False)
    token = fields.StringField(required=True, default="")
    active = fields.BooleanField(default=True)

    meta = {"db_alias": "default"}
