"""
Validation schemas using Marshmallow.
Define request/response validation schemas here.
"""
from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    """Example user schema for validation."""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PaginationSchema(Schema):
    """Schema for pagination parameters."""
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=20, validate=validate.Range(min=1, max=100))


# Initialize schema instances for reuse
user_schema = UserSchema()
users_schema = UserSchema(many=True)
pagination_schema = PaginationSchema()
