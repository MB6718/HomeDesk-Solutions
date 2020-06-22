from marshmallow import (
    Schema,
    fields
)


class UsersSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
