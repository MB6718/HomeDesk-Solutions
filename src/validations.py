from marshmallow import (
    Schema,
    fields,
    ValidationError,
)


class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UsersSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class CategoryIDField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) == float:
            raise ValidationError('ID cant be float')
        if value <= 0:
            raise ValidationError('The ID cannot be less than zero')
        else:
            return value


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
            raise ValidationError('Type must be or expenses or income')


class CreateTransactionsSchema(Schema):
    type = TypeClass(required=True, load_only=True)
    amount = fields.Float(required=True, load_only=True)
    comment = fields.Str()
    date = fields.Int()
    category_id = CategoryIDField()


class EditTransactionsSchema(Schema):
    type = TypeClass()
    amount = fields.Float()
    comment = fields.Str()
    date = fields.Int()
    category_id = fields.Int()


class CreateCategorySchema(Schema):
    name = fields.Str(required=True)
    parent_id = fields.Int()
