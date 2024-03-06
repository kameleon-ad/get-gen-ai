from marshmallow import Schema, fields, validate


class ContentValidation(Schema):
    """
    Validate body of login api
    :param
        email: string, required
        password: string, required
    Ex:
    {
        "title": "Title",
        "content": "123456aA@"
    }
    """
    title = fields.String(required=True, validate=[validate.Length(min=1, max=50)])
    content = fields.String(required=True, validate=[validate.Length(min=1)])
