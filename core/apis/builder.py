import dataclasses
import typing

import requests


class _APIBuilder:
    __URL_PATH = "https://api.bobgroganconsulting.com/api/v1"
    # __URL_PATH = "http://192.168.1.108:8500/api/v1"

    def __init__(self, action: str):
        self._action = action
        self._trigger = None
        self._eq = None

    def trigger(self, trigger):
        self._trigger = trigger
        return self

    def eq(self, **data):
        self._eq = data
        return self

    def commit(self):
        res = requests.post(
            self.__URL_PATH,
            json={
                "action": self._action,
                "trigger": self._trigger,
                "data": {
                    "eq": self._eq or {}
                }
            }
        ).json()
        return _BuilderRes(res.get("success"), res.get("data"))


@dataclasses.dataclass
class _BuilderRes:
    ok: bool
    data: typing.Any
