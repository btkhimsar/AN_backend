from mongoengine import Document, fields

from Constants.image_urls import HOME_ICON
from Constants.languages import LANGS


class User(Document):
    name = fields.StringField(max_length=30, default="")
    otp = fields.StringField(max_length=4, default="1111")
    expiry = fields.DateTimeField()
    email = fields.StringField(max_length=254, default="", required=False)
    mobile = fields.StringField(max_length=10, required=True)
    address = fields.StringField(max_length=300, default="")
    language = fields.StringField(choices=LANGS, required=False, default='ENGLISH')
    location = fields.StringField(max_length=500, default="")
    isConsumer = fields.BooleanField(default=False,)
    isProvider = fields.BooleanField(default=False)
    profile_image = fields.URLField(default=HOME_ICON)

    meta = {"db_alias": "default"}


