# coding: utf-8
import uuid
from flask_jwt_extended import decode_token, get_jwt_identity
from sqlalchemy.dialects.mysql import INTEGER
from app.extensions import SQL_DB
from app.utils import get_timestamp_now


class User(SQL_DB.Model):
    __tablename__ = 'user'

    id = SQL_DB.Column(SQL_DB.String(50), primary_key=True)
    email = SQL_DB.Column(SQL_DB.String(100))
    phone = SQL_DB.Column(SQL_DB.String(50))
    password_hash = SQL_DB.Column(SQL_DB.String(255))
    created_date = SQL_DB.Column(INTEGER(unsigned=True), default=get_timestamp_now(), index=True)
    modified_date = SQL_DB.Column(INTEGER(unsigned=True), default=0)
    is_deleted = SQL_DB.Column(SQL_DB.Boolean, default=0)
    is_active = SQL_DB.Column(SQL_DB.Boolean, default=1)

    def get_password_age(self):
        return int((get_timestamp_now() - self.modified_date_password) / 86400)

    @classmethod
    def get_current_user(cls):
        return cls.query.get(get_jwt_identity())

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


class Token(SQL_DB.Model):
    __tablename__ = 'token'

    id = SQL_DB.Column(SQL_DB.String(50), primary_key=True)
    jti = SQL_DB.Column(SQL_DB.String(36), nullable=False)
    token_type = SQL_DB.Column(SQL_DB.String(10), nullable=False)
    user_identity = SQL_DB.Column(SQL_DB.String(50), nullable=False)
    revoked = SQL_DB.Column(SQL_DB.Boolean, nullable=False)
    expires = SQL_DB.Column(INTEGER(unsigned=True), nullable=False)

    @staticmethod
    def add_token_to_database(encoded_token, user_identity):
        """
        Adds a new token to the database. It is not revoked when it is added.
        :param encoded_token:
        :param user_identity:
        """
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        expires = decoded_token['exp']
        revoked = False
        _id = str(uuid.uuid4())

        db_token = Token(
            id=_id,
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        )
        SQL_DB.session.add(db_token)
        SQL_DB.session.commit()

    @staticmethod
    def prune_database():
        """
        Delete tokens that have expired from the database.
        How (and if) you call this is entirely up you. You could expose it to an
        endpoint that only administrators could call, you could run it as a cron,
        set it up with flask cli, etc.
        """
        now_in_seconds = get_timestamp_now()
        Token.query.filter(Token.expires < now_in_seconds).delete()
        SQL_DB.session.commit()


__all__ = [
    'User',
    'Token',
]
