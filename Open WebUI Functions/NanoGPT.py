"""
title: Nano GPT 
author: Elliott Groves
version: 2.0.1
date: 2024-09-27
description: Nano GPT for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
nano_address: nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk
"""

#Nano GPT Pipeline https://openwebui.com/f/elliott/nano_gpt/
#Integrates nano-gpt.com into OpenWebUI for seamless text-based AI tasks, like document retrieval and generation.

#Nano GPT Image Generation Button https://openwebui.com/f/elliott/nanoimages/
#Allows users to generate images from text prompts with nano-gpt.com.

#Nano GPT Receive Nano Button https://openwebui.com/f/elliott/nanogpt_receive_nano/
#Automates receiving Nano cryptocurrency through OpenWebUI for use with nano-gpt.com.

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json
import time
from open_webui.utils.misc import pop_system_message


class Pipe:
    class Valves(BaseModel):
        NAME_PREFIX: str = Field(
            default="NanoGPT-2/",
            description="Prefix to be added before model names.",
        )
        NANO_GPT_API_BASE_URL: str = Field(
            default="https://nano-gpt.com/api",
            description="Base URL for accessing Nano GPT API endpoints.",
        )
        NANO_GPT_API_KEY: str = Field(
            default="Your Nano GPT API Key",
            description="API key for authenticating requests to the Nano GPT API.",
        )

    def __init__(self):
        self.type = "direct"
        self.valves = self.Valves()
        self.documents = None
        self.index = None

    async def on_startup(self):
        global documents, index

        self.documents = SimpleDirectoryReader("/app/backend/data").load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        pass

    async def on_shutdown(self):
        pass

    def pipes(self):
        if self.valves.NANO_GPT_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {self.valves.NANO_GPT_API_KEY}",
                    "Content-Type": "application/json",
                }

                response = requests.get(
                    f"{self.valves.NANO_GPT_API_BASE_URL}/models", headers=headers
                )
                response.raise_for_status()
                models = response.json()

                models_list = []
                if "text" in models.get("models", {}):
                    text_models = models["models"]["text"]
                    for model_key, model_info in text_models.items():
                        models_list.append(
                            {
                                "id": model_info.get("model"),
                                "name": f'{self.valves.NAME_PREFIX}{model_info.get("name", model_info.get("model", model_key))}',
                                "description": model_info.get("description", ""),
                                "cost": model_info.get("cost", ""),
                                "visible": model_info.get("visible", False),
                            }
                        )
                return models_list

            except Exception as e:
                return [
                    {
                        "id": "error",
                        "name": "Could not fetch models. Please check the API Key and Base URL.",
                    },
                ]
        else:
            return [
                {
                    "id": "error",
                    "name": "API Key not provided.",
                },
            ]

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        try:
            system_message, messages = pop_system_message(body["messages"])
            content_sys = system_message.get("content", "") if system_message else ""
            content_message = next((m.get("content", "") for m in messages), "")

            content = (
                content_sys
                if "Use the following context" in content_sys
                else content_message
            )
            content = (
                content.split("\n\n🪙 Cost:")[0]
                if "\n\n🪙 Cost:" in content
                else content
            )

            model_name = body.get("model", "").replace("nanogpt2.", "")

            payload = {
                "model": model_name,
                "messages": body.get("messages", []),
                "prompt": content,
            }

            headers = {
                "x-api-key": self.valves.NANO_GPT_API_KEY,
                "Content-Type": "application/json",
            }

            start_time = time.time()
            r = requests.post(
                url=f"{self.valves.NANO_GPT_API_BASE_URL}/talk-to-gpt",
                headers=headers,
                json=payload,
                timeout=120,
            )
            elapsed_time = time.time() - start_time

            r.raise_for_status()
            result = r.text

            if "<NanoGPT>" not in result:
                return f"Error from API: {result.strip()}"

            text_response, nano_info_raw = result.split("<NanoGPT>")
            text_response = text_response.strip()

            nano_info = json.loads(nano_info_raw.split("</NanoGPT>")[0])
            result2 = f"{text_response}\n\n🪙 Cost: {nano_info.get('nanoCost', 'N/A')} Nano 🪙"
            cost = nano_info.get("nanoCost", "0")

            rbo = requests.post(
                url=f"{self.valves.NANO_GPT_API_BASE_URL}/check-nano-balance",
                headers=headers,
                timeout=30,
            )
            if rbo.status_code == 200:
                rb = rbo.json()
                balance = rb.get("balance", "Error")
                resultdep = rb.get("nanoDepositAddress", "Error")
            else:
                balance = "Error"
                resultdep = "Error"

            result3 = (
                f"{result2}\n\n"
                f"🪙 Balance: {balance} Nano 🪙\n\n"
                f"🏛️ Nano Deposit Address: {resultdep} 🏛️\n\n"
                f"🌐 Website: https://nano-gpt.com/ 🌐\n\n"
                f"📌 If you make a deposit and it doesn't add to your balance, use the NanoGPTReceive action button below. "
                f"🖱️ If you still have issues, email support@nano-gpt.com 🖱️"
            )

            balance_val = float(balance)
            cost_val = float(cost)

            if balance_val < 1:
                return result3
            elif cost_val > 0.5:
                return result2
            else:
                return text_response

        except requests.exceptions.Timeout:
            return "Error: The request timed out. Please try again later."
        except requests.exceptions.HTTPError as http_err:
            return f"Error: Received HTTP status {r.status_code} from the API."
        except Exception as e:
            return f"Error: {str(e)}"
