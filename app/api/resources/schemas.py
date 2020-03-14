from marshmallow import Schema, fields

class URLSchema(Schema):
    url = fields.Url(description='URL to website')

class TaskIDSchema(Schema):
    id = fields.String(description='Task ID')

class TaskStateSchema(Schema):
    task = fields.Nested(TaskIDSchema)
    state = fields.String()