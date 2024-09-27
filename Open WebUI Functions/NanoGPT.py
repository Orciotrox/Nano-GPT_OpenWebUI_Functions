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

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json
import time
from open_webui.utils.misc import pop_system_message
from open_webui.main import chat_completion_tools_handler

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


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
            default="",
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
        # This function is called when the server is stopped.
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

                # Handle text-based models
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
                print(f"Error fetching models: {e}")
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
            processed_messages = []

            for content in system_message:
                content_sys = system_message.get("content", "")
            for message in messages:
                content_message = message.get("content", "")
            print(f"Messages: {content_message}")
            print(f"System Messages: {content_sys}")
            print(f"Body: {body}")

            if (
                "Use the following context as your learned knowledge, inside <context></context>"
                in content_sys
            ):
                content = content_sys
            else:
                content = content_message
            if "\n\n🪙 Cost:" in content:
                content = content.split("\n\n🪙 Cost:")[0]
            print(f"Content:{content}")

            processed_messages.append(
                {
                    "role": message["role"],
                    "content": content,
                }
            )

            model_name = body["model"]
            if model_name.startswith("nanogpt2."):
                model_name = model_name[len("nanogpt2.") :]

            payload = {
                "model": model_name,
                "messages": body["messages"],
                "prompt": content,
            }
            print(f"Payload:{payload}")
            # return "Stop For Testing"

            headers = {
                "x-api-key": self.valves.NANO_GPT_API_KEY,
                "Content-Type": "application/json",
            }
            print(f"Using model: {model_name}")  # Log the model name
            print(f"Payload at {current_time}: {payload}")

            # Corrected POST request
            start_time = time.time()
            r = requests.post(
                url=f"{self.valves.NANO_GPT_API_BASE_URL}/talk-to-gpt",
                headers=headers,
                json=payload,
                timeout=120,  # Increased timeout
            )
            elapsed_time = time.time() - start_time
            print(f"Request took {elapsed_time} seconds")

            # Check for HTTP errors
            r.raise_for_status()

            result = r.text
            print(f"Result Text: {result}")

            # Process the response
            if "<NanoGPT>" in result:
                parts = result.split("<NanoGPT>")
            else:
                print(f"Unexpected response format: {result}")
                return f"Error from API: {result.strip()}"

            text_response = parts[0].strip()

            # Check for title generation request
            for message in body.get("messages", []):
                if (
                    "Create a concise, 3-5 word phrase with an emoji as a title"
                    in message.get("content", "")
                ):
                    return text_response

            # Extract NanoGPT info
            try:
                nano_info = json.loads(parts[1].split("</NanoGPT>")[0])
            except (IndexError, json.JSONDecodeError) as e:
                print(f"Error parsing NanoGPT info: {e}")
                return "Error: Failed to parse NanoGPT info."

            result2 = f"{text_response}\n\n🪙 Cost: {nano_info.get('nanoCost', 'N/A')} Nano 🪙"
            cost = nano_info.get("nanoCost", "0")
            print(f"Response: {result2}")

            # Fetch balance and deposit address
            rbo = requests.post(
                url=f"{self.valves.NANO_GPT_API_BASE_URL}/check-nano-balance",
                headers=headers,
                timeout=30,  # Set a reasonable timeout
            )
            if rbo.status_code == 200:
                rb = rbo.json()
                balance = rb.get("balance", "Error")
                resultdep = rb.get("nanoDepositAddress", "Error")
            else:
                balance = "Error"
                resultdep = "Error"
                print(f"Error fetching balance: {rbo.status_code} - {rbo.text}")

            result3 = (
                f"{result2}\n\n"
                f"🪙 Balance: {balance} Nano 🪙\n\n"
                f"🏛️ Nano Deposit Address: {resultdep} 🏛️\n\n"
                f"🌐 Website: https://nano-gpt.com/ 🌐\n\n"
                f"📌 If you make a deposit and it doesn't add to your balance use the NanoGPTRecive action button below: 📌"
                f"🖱️ If you still have issues, email support@nano-gpt.com 🖱️"
            )

            # Determine final response based on balance and cost
            try:
                balance_val = float(balance)
                cost_val = float(cost)

                if balance_val < 1:
                    return result3
                elif cost_val > 0.5:
                    return result2
                else:
                    return text_response
            except ValueError:
                print(f"Invalid balance or cost values: balance={balance}, cost={cost}")
                return "Error: Invalid balance or cost value."

        except requests.exceptions.Timeout:
            print("Request to Nano GPT API timed out.")
            return "Error: The request timed out. Please try again later."
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred at {current_time}: {http_err}")
            print(f"Response text at {current_time}: {r.text}")
            return f"Error: Received HTTP status {r.status_code} from the API."
        except Exception as e:
            print(f"Unexpected error in pipe method: {e}")
            return f"Error: {str(e)}"
