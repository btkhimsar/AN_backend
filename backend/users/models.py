from mongoengine import Document, fields

from Constants.image_urls import HOME_ICON
from Constants.languages import LANGS
from Constants.user_type import USER_TYPE

class User(Document):
    name = fields.StringField(max_length=30, default="")
    expiry = fields.DateTimeField()
    email = fields.StringField(default="", required=False)
    mobile = fields.StringField(max_length=10, required=True)
    address = fields.StringField(max_length=300, default="")
    user_language = fields.StringField(choices=LANGS, required=True, default='english')
    profile_image = fields.URLField(default=HOME_ICON)
    base_location = fields.StringField(max_length=500, required=False)
    user_type = fields.StringField(choices=USER_TYPE, default="consumer", required=False)
    work_radius = fields.IntField(min_value=3, max_value=10, required=False)
    work_category = fields.StringField(min_value=1, max_length=100, required=False)

    meta = {"db_alias": "default"}
