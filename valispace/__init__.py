#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
import typing
from logging import Logger

import httpx


"""
Valispace public python API, version 2
"""


__DEBUG = True


class ValispaceException(Exception):
    pass


class Valispace:
    def __init__(
        self,
        url: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        options: typing.Optional[typing.Dict[str, typing.Union[str, typing.Any]]] = None,
    ):
        self.total_requests: int = 0

        username = options.get("username", username) if options is not None else username
        if not username:
            raise ValispaceException("Username not provided")

        password = options.get("password", password) if options is not None else password
        if not password:
            raise ValispaceException("Password not provided")

        url = options.get("url", url) if options is not None else url
        if not url:
            raise ValispaceException("URL not provided")
        else:
            url = url.strip().rstrip("/")
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "https://" + url

        t = options.get("logger", None) if options is not None else None
        if t is None and not isinstance(t, Logger):
            import logging
            self.logger: Logger = logging.getLogger("console")
        else:
            self.logger: Logger = typing.cast(Logger, t)

        self.client_id: str = typing.cast(str, options.get("client_id", "ValispaceREST")) if options is not None else "ValispaceREST"

        self.__url = url + "/rest/"
        self.__oauth_url = url + "/o/token/"

        self.logger.debug(f"URL: {self.__url}")

        self.client = httpx.AsyncClient()

        result = asyncio.run(self.client.post(self.__oauth_url, data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": self.client_id,
        }), debug=__DEBUG)

        self.logger.info(f"result: {result}")


class Project:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Component:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Vali:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Matrix:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class TextVali:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Specification:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Requirement:
    def __init__(self, valispace: Valispace):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")
