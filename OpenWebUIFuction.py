"""
title: Node Red Nano GPT Pipe
author: Orciotrox
node red flow:
Based On:
    title: OpenAI Proxy Pipe
    author: open-webui
    author_url: https://github.com/open-webui
    funding_url: https://github.com/open-webui
    version: 0.1.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Union, Generator, Iterator

import os
import json
import requests


class Pipe:
    class Valves(BaseModel):
        NAME_PREFIX: str = Field(
            default="NanoGPT/",
            description="Prefix to be added before model names.",
        )
        OPENAI_API_BASE_URL: str = Field(
            default="",
            description="Base URL for accessing Node Red"
            """ex. http://192.168.1.1:1880""",
        )
        OPENAI_API_KEY: str = Field(
            default="",
            description="API key for authenticating requests to the Nano-GPT API.",
        )
        pass

    def __init__(self):
        self.type = "manifold"
        self.valves = self.Valves()
        pass

    def pipes(self):
        if self.valves.OPENAI_API_KEY:
            try:
                headers = {}
                headers["Authorization"] = f"Bearer {self.valves.OPENAI_API_KEY}"
                headers["Content-Type"] = "application/json"

                r = requests.get(
                    f"{self.valves.OPENAI_API_BASE_URL}/models", headers=headers
                )

                models = r.json()
                return [
                    {
                        "id": model["id"],
                        "name": f'{self.valves.NAME_PREFIX}{model["name"] if "name" in model else model["id"]}',
                    }
                    for model in models["data"]
                ]

            except Exception as e:

                print(f"Error: {e}")
                return [
                    {
                        "id": "error",
                        "name": "Could not fetch model, please update the API Key in the valves.",
                    },
                ]
        else:
            return [
                {
                    "id": "error",
                    "name": "API Key not provided.",
                },
            ]

    def pipe(self, body: dict, __user__: dict) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")

        headers = {
            "Authorization": f"Bearer {self.valves.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        model_id = body["model"][body["model"].find(".") + 1 :]
        payload = {**body, "model": model_id}

        try:
            r = requests.post(
                url=f"{self.valves.OPENAI_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                stream=False,
            )

            r.raise_for_status()

            if body.get("stream", False):
                result = r.iter_lines()
            else:
                result = r.json()

            # Process the result to replace LINEBREAKHERE with \n
            if isinstance(result, str):
                result = result.replace("LINEBREAKHERE", "\n")
            elif isinstance(result, dict):
                result_str = json.dumps(result)
                result_str = result_str.replace("LINEBREAKHERE", "\n")
                result = json.loads(result_str)
            elif isinstance(result, Generator) or isinstance(result, Iterator):
                result = (line.replace(b"LINEBREAKHERE", b"\n") for line in result)

            return result

        except Exception as e:
            return f"Error: {e}"
