from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    # account_created_date = fields.DateTime(dump_only=True)
    is_staff = fields.Bool(required=True)

class UserLogInOutSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class PlainCircleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_by_id = fields.Int()
    created_at = fields.DateTime()

class UserSchema(PlainUserSchema):
    circles = fields.List(fields.Nested(PlainCircleSchema()), dump_only=True)

class CircleSchema(PlainCircleSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

#CircleAndUserSchema is used to return information about both the Item and Tag that have been modified in an endpoint, together with an informative message.
class CircleAndUserSchema(Schema):
    user = fields.List(fields.Nested(PlainUserSchema))
    circle = fields.Nested(PlainCircleSchema)


class CircleMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    role = fields.Str(required=False, load_default="member")







