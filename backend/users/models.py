from mongoengine import Document, fields
from Constants.image_urls import HOME_ICON
from Constants.languages import LANGS
from Constants.user_type import USER_TYPE


class User(Document):
    mobile = fields.StringField(max_length=10, required=True)
    name = fields.StringField(max_length=30, required=True)
    user_type = fields.StringField(choices=USER_TYPE, required=True, default="consumer")
    user_language = fields.StringField(choices=LANGS, required=True, default='english')
    email = fields.StringField(max_length=50, required=False)
    address = fields.StringField(max_length=100, required=False)
    profile_image = fields.URLField(default=HOME_ICON)
    work_category = fields.StringField(max_length=50, required=False)
    base_location = fields.PointField(required=False)
    work_radius = fields.IntField(min_value=3, max_value=10, required=False)
    token = fields.StringField(max_length=200, required=True)
    active = fields.BooleanField(required=False, default=True)

    meta = {"db_alias": "default"}
