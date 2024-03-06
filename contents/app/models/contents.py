from app.extensions import SQL_DB


class Content(SQL_DB.Model):
    __tablename__ = 'content'

    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True, autoincrement=True)
    title = SQL_DB.Column(SQL_DB.String(64), nullable=False)
    content = SQL_DB.Column(SQL_DB.Text(), nullable=False)
    status = SQL_DB.Column(SQL_DB.Boolean(), default=False)
    created_by = SQL_DB.Column(SQL_DB.String(50), nullable=False)
    modified_by = SQL_DB.Column(SQL_DB.String(50), nullable=True)

    @staticmethod
    def create(title, content, created_by, **kwargs):
        try:
            new_content = Content(title=title, content=content, created_by=created_by, **kwargs)
            SQL_DB.session.add(new_content)
            SQL_DB.session.commit()
        except:
            SQL_DB.session.rollback()
            raise
        return new_content

    @staticmethod
    def retrieve_all(raw_format=True):
        contents = Content.query.all()
        if raw_format:
            return [content.raw for content in Content.query.all()]
        return contents

    @property
    def raw(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
        }


__all__ = [
    'Content',
]
