"""
The module designed to contain all logic related to authentication.
"""

import datetime
from functools import wraps
import os

from flask import request
import jwt
from werkzeug.exceptions import Unauthorized
from werkzeug.security import check_password_hash

from coa_flask_app.db_accessor import Accessor


def login(username: str, password: str) -> str:
    """
    A login function to handle authentication.

    Args:
        username: The username of person trying to login.
        password: The password of the person trying to login.

    Returns:
        The JWT if there are authorized.

    Raises:
        This can raise Unauthorized errors if the login attempt fails.
    """
    query = """
            SELECT
                password
            FROM coa.ab_user AS cau
            WHERE
                cau.username = %s AND
                cau.active = 1
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (username,))
        record = db_handle.fetchone()

        if record is None or not check_password_hash(record["password"], password):
            raise Unauthorized()

        return str(
            jwt.encode(
                {
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(days=0, hours=6),
                    "iat": datetime.datetime.utcnow(),
                    "sub": username,
                },
                os.environ["SECRET_KEY"],
                algorithm="HS256",
            )
        )


def verify_token(func):
    """
    A decorator used for the flask routes to add authentication checks.
    """

    @wraps(func)
    def _inner():
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized("No provided token. Please login.")

        auth_token = auth_header.split(" ")[1]
        try:
            jwt.decode(auth_token, os.environ["SECRET_KEY"])
        except jwt.ExpiredSignatureError as err:
            raise Unauthorized("Signature expired. Please log in again.") from err
        except jwt.InvalidTokenError as err:
            raise Unauthorized("Invalid token. Please log in again.") from err

        return func()

    return _inner
