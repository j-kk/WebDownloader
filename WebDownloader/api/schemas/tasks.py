from marshmallow import Schema, fields, post_load

class TaskId(object):
    id: str

    def __init__(self, id: str):
        self.id = id


class TaskIdSchema(Schema):
    id = fields.List(fields.String(), required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return [TaskId(id) for id in data['id']]



class WebsiteURLSchema(Schema):
    url = fields.List(fields.URL(), required=True)
    @post_load
    def make_url(self, data, **kwargs):
        return data['url']
