from marshmallow import Schema, fields

class PlainItemSchemas(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)
    


class PlainStoreSchemas(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required = True)
    


class ItemUpdateSchemas(Schema):
    name = fields.Str()
    price = fields.Str()

class ItemSchemas(PlainItemSchemas):
    store_id = fields.Int(required = True, load_only=True)
    store = fields.Nested(PlainStoreSchemas(), dump_only=True)

class StoreSchemas(PlainStoreSchemas):
    item = fields.List(fields.Nested(PlainItemSchemas()), dump_only= True)