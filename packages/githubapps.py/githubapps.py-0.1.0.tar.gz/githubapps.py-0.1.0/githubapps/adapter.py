import json
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union
import jwt
import aiohttp
import datetime
import requests
import re
import urllib.parse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import pprint

from .errors import (BadRequest, Forbidden, HTTPException, InternalServerError,
                     NotFound, PayloadTooLarge, QuotaExceeded,
                     ServiceUnavailable, TooManyRequests, URITooLong)

__all__ = ['Authentication', 'Auth']


class Authentication(metaclass=ABCMeta):
    def __init__(self, app_id: int, installation_id: int, client_secret, *, iat: int = 30, exp: int = 30):
        self.installation_id = installation_id
        self.endpoint = 'https://api.github.com/app/installations/{}/access_tokens'.format(
            self.installation_id)
        self.algorithm = "RS256"
        self.app_id = app_id
        self.client_secret = client_secret
        self.iat = iat
        self.exp = exp
        self.now = datetime.datetime.now(datetime.timezone.utc)

    @abstractmethod
    def gen_jwt(self) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def gen_pubkey(self) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def is_authorization(self, _jwt: str, client_public: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_access_token_response(self, jwt: str, **kwargs) -> Optional[Union[list, dict]]:
        raise NotImplementedError()

    @abstractmethod
    def get_access_token(self, *, access_token_response: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_usage(self) -> dict:
        raise NotImplementedError()

    def _check_status(self, status_code, response, data) -> Union[dict, list]:
        if 200 <= status_code < 300:
            return data
        message = data.get('message', '') if data else ''
        if status_code == 400:
            raise BadRequest(response, message)
        elif status_code == 403:
            raise Forbidden(response, message)
        elif status_code == 404:
            raise NotFound(response, message)
        elif status_code == 413:
            raise PayloadTooLarge(response, message)
        elif status_code == 414:
            raise URITooLong(response, message)
        elif status_code == 429:
            raise TooManyRequests(response, message)
        elif status_code == 456:
            raise QuotaExceeded(response, message)
        elif status_code == 503:
            raise ServiceUnavailable(response, message)
        elif 500 <= status_code < 600:
            raise InternalServerError(response, message)
        else:
            raise HTTPException(response, message)


class Auth(Authentication):
    """Researchmap authentication interface.

    Parameters
    ----------
    app_id: :class:`str`
      Client ID.
    client_secret: :class:`bytes`
      Client secret key.

    Keyword Arguments
    -----------------
    iat: :class:`int`
      Issued at [sec].
    exp: :class:`int`
      Expire at [sec].
    trial: :class:`bool`
      Trial mode.
    """

    @property
    def is_trial(self) -> bool:
        """Get trial mode.

        Returns
        -------
        :class:`bool`
          Trial mode.
        """
        return self.trial

    @property
    def time_now(self) -> datetime.datetime:
        """Get current time [aware].

        Returns
        -------
        :class:`datetime.datetime`
          Current time of UTC.
        """
        return self.now

    @property
    def time_iat(self) -> datetime.datetime:
        """Get issued at time [aware].

        Returns
        -------
        :class:`datetime.datetime`
          Issued at time of UTC.
        """
        return self.now - datetime.timedelta(seconds=self.iat)

    @property
    def time_exp(self) -> datetime.datetime:
        """Get expire at time [aware].

        Returns
        -------
        :class:`datetime.datetime`
          Expire at time of UTC.
        """
        return self.now + datetime.timedelta(seconds=self.exp)

    @property
    def token(self) -> str:
        """Get token.

        Returns
        -------
        :class:`str`
          Token.

        Raises
        ------
        :exc:`InvalidToken`
          Invalid token.
        :class:`json.JSONDecodeError`
          JSON decode error.
        :class:`requests.exceptions.HTTPError`
          HTTP error.
        """
        return self.get_access_token()

    def gen_jwt(self, *, exp: int = None, iat: int = None) -> bytes:
        """Generate JWT.

        Keyword Arguments
        -----------------
        exp: :class:`int`
          Expire at [sec].
        iat: :class:`int`
          Issued at [sec].

        Returns
        -------
        :class:`bytes`
          JWT.
        """
        if exp is None:
            exp = self.exp
        if iat is None:
            iat = self.iat

        payload = {
            "iss": self.app_id,
            "iat": self.now - datetime.timedelta(seconds=iat),
            "exp": self.now + datetime.timedelta(seconds=exp),
        }
        _jwt = jwt.encode(payload, self.client_secret,
                          algorithm=self.algorithm)
        return _jwt

    def gen_pubkey(self, *, client_secret: str = None) -> bytes:
        """
        Generate public key.

        Keyword Arguments
        -----------------
        client_secret: :class:`str`
          Client secret key.

        Returns
        -------
        :class:`bytes`
           Client public key.
        """
        if client_secret is None:
            client_secret = self.client_secret

        privkey = serialization.load_pem_private_key(
            client_secret,
            password=None,
            backend=default_backend()
        )
        pubkey = privkey.public_key()
        client_public = pubkey.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return client_public

    def is_authorization(self, *, _jwt: str = None, client_public: str = None) -> bool:
        """Check authorization.

        Keyword Arguments
        -----------------
        _jwt: :class:`str`
          JWT.
        client_public: :class:`str`
          Client public key.

        Returns
        -------
        :class:`bool`
          True if authorization.

        Raises
        ------
        :class:`jwt.InvalidTokenError`
          Invalid JWT.

        """
        if _jwt is None:
            _jwt = self.gen_jwt()
        if client_public is None:
            client_public = self.gen_pubkey()

        try:
            decoded_jwt = jwt.decode(
                _jwt, key=client_public, algorithms=self.algorithm)
            if decoded_jwt['iss'] == self.app_id:
                return True
        except:
            print("The signature of JWT cannot be verified.")
            return False

    def get_access_token_response(self, *, _jwt: bytes = None, **kwargs) -> Optional[Union[list, dict]]:
        """Get access token.

        Keyword Arguments
        ----------
        _jwt: :class:`bytes`
          JWT.

        Returns
        -------
        Optional[Union[:class:`list`, :class:`dict`]]
          Access token.

        Raises
        ------
        :exc:`HTTPException`
          An unknown HTTP related error occurred, usually when it isn’t 200 or the known incorrect credentials passing status code.
        """
        if _jwt is None:
            _jwt = self.gen_jwt()

        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'Bearer {}'.format(_jwt),
        }
        if self.is_authorization():
            req_access_token = requests.post(
                url=self.endpoint, headers=headers)
            try:
                data = req_access_token.json()
            except json.JSONDecodeError:
                print(req_access_token.content)
            return self._check_status(req_access_token.status_code, req_access_token, data)
        else:
            print("Access Token is not valid")

    def get_access_token(self, *, access_token_response: Optional[Union[list, dict]] = None) -> str:
        """Get access token.

        Keyword Arguments
        ----------
        access_token_response: :class: Optional[Union[:class:`list`, :class:`dict`]]
          Access token response.

        Returns
        -------
        :class:`str`
          Access token.

        Raises
        ------
        :class:`TypeError`
          The type of the argument is not correct.
        :exc:`HTTPException`
          An unknown HTTP related error occurred, usually when it isn’t 200 or the known incorrect credentials passing status code.
        :exc:`InvalidToken`
          Invalid token.
        """
        if access_token_response is None:
            access_token_response = self.get_access_token_response()
        return access_token_response["token"]

    def get_usage(self) -> None:
        return None
