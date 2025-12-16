from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a note."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating a note."""
    title = fields.Str(required=False, validate=validate.Length(min=1, max=255), description="Title of the note")
    content = fields.Str(required=False, validate=validate.Length(min=1), description="Content/body of the note")


# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for a note resource."""
    id = fields.Int(required=True, description="Unique identifier of the note")
    title = fields.Str(required=True, description="Title of the note")
    content = fields.Str(required=True, description="Content/body of the note")
    created_at = fields.DateTime(required=True, description="Creation timestamp (UTC, ISO8601)")
    updated_at = fields.DateTime(required=True, description="Last update timestamp (UTC, ISO8601)")
