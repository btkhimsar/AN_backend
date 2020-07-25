from mongoengine import Document, fields
from Constants.image_urls import HOME_ICON
from Constants.colors import *


class SubCategory(Document):
    category_id = fields.IntField(min_value=11, max_value=99)
    super_category_id = fields.IntField(min_value=1, max_value=9)
    description = fields.StringField(max_length=200, default="Description String Here")
    img_url = fields.URLField(default=HOME_ICON)
    type = fields.StringField(default="")
    tg = fields.IntField()


class Category(Document):
    name = fields.StringField(max_length=200, default="Category String Here...")
    description = fields.StringField(max_length=200, default="Description String Here...")
    super_category_id = fields.IntField(min_value=1, max_value=9)
    img_url = fields.URLField(default=HOME_ICON)
    bg_Color = fields.StringField(default=PINK)
    category = fields.ListField(SubCategory())
