from marshmallow import (
    Schema,
    fields,
    ValidationError,
)

class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UsersSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

class TypeClass(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            name = {
                'expenses': 'expenses',
                'income': 'income',
            }[value]
            if name:
                return name
            else:
                raise ValidationError
        except:
             raise ValidationError('Тип должен быть или expenses - расходы, или income - доходы')

class TransactionSchema(Schema):
    type = TypeClass()
    amount = fields.Float()
    comment = fields.Str()
    date = fields.TimeDelta()
    category_id = fields.Int()
