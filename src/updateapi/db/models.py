from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, LongField, URLField, IntField, EmbeddedDocumentField
from mongoengine.fields import ListField

class Package(EmbeddedDocument):
    version = StringField(required=True)
    incremental_version = StringField(required=True)
    datetime = LongField(required=True)
    filename = StringField(required=True)
    package_id = StringField(required=True)
    build_flavour = StringField(required=True)
    size = LongField(required=True)
    url = URLField(required=True)
    package_type = StringField(required=True)
    
class Device(Document):
    name = StringField(required=True)
    codename = StringField(required=True)
    n_packages = IntField(required=True)
    packages = ListField(EmbeddedDocumentField(Package), required=True)

class Token(Document):
    secret = StringField(required=True)
    expire = LongField(required=True)

