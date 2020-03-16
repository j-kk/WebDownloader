from marshmallow import Schema, fields

class URLSchema(Schema):
    url = fields.Url(description='URL to website', required=True)

class TaskIDSchema(Schema):
    class Meta:
        fields = ('id')
    id = fields.String(description='Task ID', required=True)

class TaskStateSchema(Schema):
    task = fields.Nested(TaskIDSchema)
    state = fields.String()

