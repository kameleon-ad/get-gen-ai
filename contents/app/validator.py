from marshmallow import Schema, fields, validate


class ContentValidation(Schema):
    """
    Validate body of login api
    :param
        title: string, required
        content: string, required
    Ex:
    {
        "title": "Title",
        "content": "123456aA@"
    }
    """
    title = fields.String(required=True, validate=[validate.Length(min=1, max=50)])
    content = fields.String(required=True, validate=[validate.Length(min=1)])


class ReviewValidation(Schema):
    """
    Validate body of login api
    :param
        review: string, required
    Ex:
    {
        "review": "review"
    }
    """
    review = fields.String(required=True, validate=[validate.Length(min=1)])
