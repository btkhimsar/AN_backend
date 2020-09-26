from mongoengine import Document, fields, EmbeddedDocument
from Constants.image_urls import HOME_ICON
from Constants.languages import LANGS
from Constants.user_type import USER_TYPE


class ProviderInfo(EmbeddedDocument):
    is_active = fields.BooleanField(required=False, default=True)
    sent_interests = fields.ListField(fields.LongField(), required=False)
    loc_name = fields.StringField(max_length=100, required=False)
    loc = fields.PointField(required=False)
    category = fields.IntField(required=False)
    radius = fields.IntField(default=5, required=False)
    complaints_count = fields.IntField(required=False, default=0)


class User(Document):
    _id = fields.LongField(primary_key=True)
    mobile = fields.StringField(max_length=10, required=True)
    name = fields.StringField(max_length=30, required=True)
    user_type = fields.StringField(choices=USER_TYPE, required=True, default="consumer")
    language = fields.StringField(choices=LANGS, required=True, default='english')
    email = fields.StringField(max_length=50, required=False)
    pic_url = fields.URLField(default=HOME_ICON, required=False)
    fcm_token = fields.StringField(max_length=200, required=True)
    my_requests = fields.ListField(fields.LongField())
    provider_info = fields.EmbeddedDocumentField(ProviderInfo)
    rating = fields.FloatField(required=False)

    meta = {"db_alias": "default"}
