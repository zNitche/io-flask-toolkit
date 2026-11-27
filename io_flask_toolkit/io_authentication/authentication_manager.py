import secrets
from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime
from flask import g, session
from io_flask_toolkit.io_extras import InMemoryDatabase
from io_flask_toolkit.io_authentication.models.base_user_model import BaseUserModel 


@dataclass
class AuthDbItem:
    created_at: str
    id: str
    ip_address: str | None


@dataclass
class UserSessionsDetails:
    key: str
    ttl: int
    value: AuthDbItem
    is_current: bool


class AuthenticationManager:
    def __init__(self, auth_db: InMemoryDatabase,
                 user_model: type[BaseUserModel],
                 logged_in_route: str,
                 password_authentication_route: str | None = None):

        self.user_model = user_model

        self.logged_in_route = logged_in_route
        self.password_authentication_route = password_authentication_route

        self.__default_auth_token_ttl = 600
        self.__auth_db = auth_db

    def setup(self, default_auth_token_ttl: None | int = 600):
        if default_auth_token_ttl is not None:
            self.__default_auth_token_ttl = default_auth_token_ttl

    def get_auth_db_key_pattern(self, token: str | None = None, user_id: int | None = None):
        return f"user:{'(.*)' if user_id is None else user_id}:{'(.*)' if token is None else token}:"

    def login(self, user_id: int, remote_addr: str | None = None):
        token = secrets.token_hex(128)

        auth_db_key = self.get_auth_db_key_pattern(
            user_id=user_id, token=token)
        value = AuthDbItem(created_at=datetime.now().isoformat(),
                           id=uuid4().hex, ip_address=remote_addr)

        self.__auth_db.set_value(
            key=auth_db_key, value=value.__dict__, ttl=self.__default_auth_token_ttl)

        session["io_auth_token"] = token

    def refresh(self, token: str, user_id: int):
        auth_db_key = self.get_auth_db_key_pattern(
            user_id=user_id, token=token)

        self.__auth_db.update_ttl(
            key=auth_db_key, ttl=self.__default_auth_token_ttl)

    def logout(self):
        token = session.get("io_auth_token")
        current_user = self.current_user

        if token is not None and current_user:
            self.remove_auth_token(token=token, user_id=current_user.id)

        self.clear_session()

    def remove_auth_token(self, token: str, user_id: int | None = None, via_pattern: bool = True):
        if via_pattern:
            token = self.get_auth_db_key_pattern(token=token, user_id=user_id)

        self.__auth_db.delete_key(token)

    def token_exists(self, token: str):
        key = self.__auth_db.get_value(
            pattern=self.get_auth_db_key_pattern(token=token))

        return True if key is not None else False

    @property
    def current_user(self) -> BaseUserModel:
        return g.get("io_current_user", None)

    def user_for_token(self, token: str | None) -> BaseUserModel | None:
        if not token:
            return None

        if ":" in token:
            raise Exception("':' not allowed in auth token")

        auth_key = self.__auth_db.get_key_for_pattern(
            pattern=self.get_auth_db_key_pattern(token=token))

        if not auth_key:
            return None

        split_key = auth_key.split(":")
        # remove last empty string
        split_key.pop()

        # some extra check
        if len(split_key) != 3:
            return None

        user_id = int(split_key[1])

        user = BaseUserModel.query().filter_by(id=user_id).first()

        return user

    def get_auth_token_for_current_session(self):
        return session.get("io_auth_token")

    def get_last_password_authentication(self):
        iso_string = session.get("io_last_password_authentication")

        if iso_string is not None:
            iso_string = datetime.fromisoformat(iso_string)

        return iso_string

    def set_password_authentication_origin(self, origin_url: str | None, referrer_url: str | None):
        session["io_password_authentication_origin"] = origin_url
        session["io_password_authentication_referrer"] = referrer_url

    def get_password_authentication_origin(self):
        origin_url = session.get("io_password_authentication_origin")
        referrer_url = session.get("io_password_authentication_referrer")

        return origin_url, referrer_url

    def set_last_password_authentication(self):
        now = datetime.now().isoformat()
        session["io_last_password_authentication"] = now

        self.set_password_authentication_origin(
            origin_url=None, referrer_url=None)

    def get_active_tokens_for_user(self, user_id: int):
        tokens = self.__auth_db.get_all_keys_for_pattern(
            pattern=self.get_auth_db_key_pattern(user_id=user_id))

        return tokens

    def __get_auth_db_user_metadata(self, user_id: int):
        keys = self.__auth_db.get_all_keys_for_pattern(
            pattern=self.get_auth_db_key_pattern(user_id=user_id))

        current_token = self.get_auth_token_for_current_session()
        current_auth_key = self.get_auth_db_key_pattern(
            token=current_token, user_id=user_id)

        return keys, current_token, current_auth_key

    def get_user_sessions(self, user_id: int):
        sessions = []

        keys, current_token, current_auth_key = self.__get_auth_db_user_metadata(
            user_id=user_id)

        for key in keys:
            data = self.__auth_db.get_value(key=key)
            ttl = self.__auth_db.get_ttl(key)

            if data:
                sessions.append(UserSessionsDetails(key=key,
                                                    ttl=int(ttl) if ttl else 0,
                                                    value=AuthDbItem(**data),
                                                    is_current=key == current_auth_key))

        return sessions

    def get_user_session_by_id(self, user_id: int, id: str):
        s = None

        keys, current_token, current_auth_key = self.__get_auth_db_user_metadata(
            user_id=user_id)

        for key in keys:
            data = self.__auth_db.get_value(key=key)
            ttl = self.__auth_db.get_ttl(key)

            if data:
                value = AuthDbItem(**data)

                if value.id == id:
                    s = UserSessionsDetails(key=key,
                                            ttl=int(ttl) if ttl else 0,
                                            value=value,
                                            is_current=key == current_auth_key)

                    break

        return s

    def clear_session(self, complete_wipe=False):
        if complete_wipe:
            session.clear()

        else:
            lang = session.get("io_lang")
            session.clear()

            session["io_lang"] = lang
