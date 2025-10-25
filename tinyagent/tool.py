# -*- coding: utf-8 -*-

import json

from pydantic import BaseModel
from typing import Callable

class Signature(BaseModel):
    pass

class Tool:

    name: str
    description: str
    function: Callable
    signature: type[Signature]

    def call(self, **kwargs) -> str:
        # When assigned, self.function becomes a bound method.
        # Extract the plain function to avoid calling with self.
        function = self.function.__func__ # type: ignore
        validated = self.signature(**kwargs)
        return function(**validated.model_dump())

    @property
    def schema(self) -> dict:
        if not self.name.isidentifier():
            raise ValueError(f"Bad {self.name=}")
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.signature.model_json_schema(),
        }

    @property
    def schema_json(self) -> str:
        return json.dumps(self.schema, ensure_ascii=False, indent=2)
