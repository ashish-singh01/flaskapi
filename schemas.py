from marshmallow import Schema, fields

class PlainItemSchemas(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)
    


class PlainStoreSchemas(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    
class PlainTagSchemas(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchemas(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchemas(PlainItemSchemas):
    store_id = fields.Int(required = True)
    store = fields.Nested(PlainStoreSchemas(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchemas), dump_only=True)

class StoreSchemas(PlainStoreSchemas):
    item = fields.List(fields.Nested(PlainItemSchemas()), dump_only= True)
    tags = fields.List(fields.Nested(PlainTagSchemas()), dump_only=True)

class TagSchemas(PlainTagSchemas):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchemas()), dump_only=True)
    store = fields.Nested(PlainStoreSchemas(), dump_only=True)


class TagAndItemSchemas(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchemas)
    tag = fields.Nested(TagSchemas)




class UserSchemas(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)