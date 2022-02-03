#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import asyncio
import typing
import logging

import httpx


"""
Valispace public python API Lite
"""


logging.basicConfig(level=logging.DEBUG)


class ValispaceException(Exception):
    pass


class Valispace:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        **params,
    ):
        if not username or len(username) == 0:
            raise ValispaceException("Username not provided")
        else:
            self.__username = username

        if not password or len(password) == 0:
            raise ValispaceException("Password not provided")
        else:
            self.__password = password

        if not url or len(url) == 0:
            raise ValispaceException("URL not provided")
        else:
            url = url.strip().rstrip("/")
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "https://" + url
            self.__url = url + "/rest/"
            self.__oauth_url = url + "/o/token/"

        self.__total_requests: int = 0
        self.__client = None

        self.__client_id: str = typing.cast(str, params.get("client_id", "ValispaceREST"))
        self.__default_project = params.get("project", None)

        t = params.get("logger", None)
        if t is None and not isinstance(t, logging.Logger):
            self.logger: logging.Logger = logging.getLogger("console")
        else:
            self.logger: logging.Logger = typing.cast(logging.Logger, t)

        self.login()

        self.logger.info(f"result: {result}")

    def __login(self):
        post_data = {
            "grant_type": "password",
            "username": self.__username,
            "password": self.__password,
            "client_id": self.__client_id,
        }

        if self.__client:
            self.__client.close()

        self.__client = httpx.Client()

        response = self.__client.post(self.__oauth_url, data=post_data, headers={})
        response_data = response.json()

        if "error" in response_data and response_data["error"] != None:
            if "error_description" in response_data:
                raise ValispaceException(response_data["error_description"])
            else:
                raise ValispaceException(response_data["error"])

        self.__client.headers = {
            "Authorization": f"Bearer {response_data['access_token']}",
            "Content-Type": "application/json"
        }

        return True


    def __del__(self):
        self.__client.aclose()


    def __request(self):
        self.__total_requests += 1
        if self.__total_requests > 200:
            pass
        pass

    def get_valis(self, **params):
        response = self.__client.get(self.__url + "valis/")
        return response


class Project:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Component:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Vali:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Matrix:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class TextVali:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Specification:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")


class Requirement:
    def __init__(self, valispace: Valispace, data: typing.Dict[str, typing.Any]):
        if not valispace:
            raise ValispaceException("valispace instance can't be none")
