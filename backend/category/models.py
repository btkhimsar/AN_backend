from mongoengine import Document, fields
from Constants.image_urls import HOME_ICON
from Constants.colors import *

class Category(Document):
    name = fields.MapField(fields.StringField())
    description = fields.MapField(fields.StringField())
    icon_url = fields.URLField(max_length=200, required=True, default=HOME_ICON)
    has_questions = fields.BooleanField(required=True, default=False)

class SuperCategory(Document):
    name = fields.MapField(fields.StringField(max_length=100, default="", required=True), required=True)
    description = fields.MapField(fields.StringField(max_length=100, default="", required=True), required=True)
    default_view_count = fields.StringField(max_length=20, default="10")
    categories = fields.ListField(fields.StringField(max_length=200))
