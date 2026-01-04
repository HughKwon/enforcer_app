from marshmallow import Schema, fields, validates, ValidationError


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

# class CircleAndUserSchema(Schema):
#     user = fields.Nested(UserSchema, many=True)
#     circle = fields.Nested(CircleSchema)

class CircleMemberRemoveSchema(Schema):
    message = fields.Str()
    user = fields.Str()
    circle = fields.Str()

class CircleMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    role = fields.Str(required=False, load_default="member")

class SendCircleMessageSchema(Schema):
    message = fields.Str()

class CircleMessageSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(PlainUserSchema, only=("id", "username"), dump_only=True)

class GetCircleMessagesSchema(Schema):
    messages = fields.List(fields.Nested(CircleMessageSchema))

class GoalUpdateSchema(Schema):
    circle_id = fields.Str(required=False)
    title = fields.Str(required=False)
    description = fields.Str(required=False)
    goal_type = fields.Str(required=False)
    start_date = fields.DateTime(required=False)
    is_active = fields.Boolean(required=False)

class FollowingSchema(Schema):
    followings = fields.List(fields.Nested(PlainUserSchema()))

# class FollowingSchema(Schema):
#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True)

class FollowersSchema(Schema):
    followers = fields.List(fields.Nested(PlainUserSchema))

class TargetSchema(Schema):
    id = fields.Int(dump_only=True)
    goal_id = fields.Int(required=False)
    user_id = fields.Int()
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    is_completed = fields.Boolean(required=False, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime()
    completed_at = fields.DateTime()

class PlainGoalSchema(Schema):
    id = fields.Int(dump_only=True)
    circle_id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    goal_type = fields.Str(required=False, load_default="daily")
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    is_active = fields.Boolean(required=False, load_default=False)
    created_at = fields.DateTime(dump_only=True)

    @validates('goal_type')
    def validate_goal_type(self, value, **kwargs):
        """Validate that goal_type is one of the allowed types."""
        from models import GoalModel
        if value not in GoalModel.VALID_TYPES:
            raise ValidationError(
                f"Invalid goal type. Must be one of: {', '.join(GoalModel.VALID_TYPES)}"
            )

class GoalSchema(PlainGoalSchema):
    user = fields.Nested(PlainUserSchema, dump_only=True)
    circle = fields.Nested(PlainCircleSchema, dump_only=True)
    targets = fields.List(fields.Nested(TargetSchema))

class PlainCheckInSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)

class PlainReactSchema(Schema):
    id = fields.Int(dump_only=True)
    react_type = fields.Str(required=False)

class PlainCheckInCommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

class ReactSchema(PlainReactSchema):
    check_in = fields.Nested(PlainCheckInSchema, dump_only=True, required=False)
    comment = fields.Nested(PlainCheckInCommentSchema, dump_only=True, required=False)
    user = fields.Nested(PlainUserSchema, dump_only=True, required=False)

class CheckInSchema(PlainCheckInSchema):
    user = fields.Nested(PlainUserSchema, dump_only=True)
    goal = fields.Nested(PlainGoalSchema, dump_only=True, required=False)
    target = fields.Nested(TargetSchema, dump_only=True, required=False)
    reacts = fields.List(fields.Nested(PlainReactSchema))

class CheckInListSchema(Schema):
    check_ins = fields.List(fields.Nested(PlainCheckInSchema))

class CheckInCommentSchema(PlainCheckInCommentSchema):
    # check_in = fields.Nested(PlainCheckInSchema, dump_only=True)
    user = fields.Nested(PlainUserSchema, dump_only=True)
    reacts = fields.List(fields.Nested(PlainReactSchema))

class CheckInCommentListSchema(Schema):
    fields.List(fields.Nested(CheckInCommentSchema))

class FeedSchema(Schema):
    feed = fields.List(fields.Nested(CheckInSchema))

class LeaderboardEntrySchema(Schema):
    user_id = fields.Int()
    username = fields.Str()
    total_check_ins = fields.Int()
    active_goals = fields.Int()
    last_check_in = fields.DateTime(allow_none=True)
    member_since = fields.DateTime()
    role = fields.Str()

class CircleLeaderboardSchema(Schema):
    circle_id = fields.Int()
    circle_name = fields.Str()
    leaderboard = fields.List(fields.Nested(LeaderboardEntrySchema))

class BuddyRequestCreateSchema(Schema):
    message = fields.Str(required=False)

class BuddyRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    from_user_id = fields.Int(dump_only=True)
    to_user_id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    responded_at = fields.DateTime(dump_only=True)
    from_user = fields.Nested(PlainUserSchema, dump_only=True)
    to_user = fields.Nested(PlainUserSchema, dump_only=True)

    # Add flat username fields for convenience
    requester_id = fields.Method("get_requester_id")
    requester_username = fields.Method("get_requester_username")
    receiver_id = fields.Method("get_receiver_id")
    receiver_username = fields.Method("get_receiver_username")

    def get_requester_id(self, obj):
        return obj.from_user_id

    def get_requester_username(self, obj):
        return obj.from_user.username if obj.from_user else None

    def get_receiver_id(self, obj):
        return obj.to_user_id

    def get_receiver_username(self, obj):
        return obj.to_user.username if obj.to_user else None

class BuddyInfoSchema(Schema):
    user_id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    buddies_since = fields.DateTime()

class BuddyListSchema(Schema):
    buddies = fields.List(fields.Nested(BuddyInfoSchema))












