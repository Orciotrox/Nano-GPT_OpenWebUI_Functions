""""
title: Nano GPT 
author: Elliott Groves
version: 1.0.2
date: 2024-10-10
description: Nano GPT for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
import requests
import json
import time
from open_webui.utils.misc import pop_system_message
from open_webui.main import chat_completion_tools_handler
from open_webui.config import get_config, save_config, BannerModel

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
            default="Your NanoGPT API Key",
            description="API key for authenticating requests to the Nano GPT API.",
        )

    def __init__(self):
        self.type = "direct"
        self.valves = self.Valves()
        self.documents = None
        self.index = None

    async def on_startup(self):
        # Initialize resources if needed
        pass

    async def on_shutdown(self):
        # Clean up resources if needed
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

    async def pipe(
        self, body: dict, __event_emitter__=None
    ) -> Union[str, Generator, Iterator]:
        try:
            system_message, messages = pop_system_message(body["messages"])

            # Initialize content_sys and content_message with default values
            content_sys = ""
            content_message = ""
            # Check if system_message and messages are not None
            if system_message is None:
                system_message = {}  # Default to an empty dict
            if messages is None:
                messages = []  # Default to an empty list

            # Extract content from system message if present
            for content in system_message:
                content_sys = system_message.get("content", "")

            # Extract content from user/assistant messages
            for message in messages:
                content_message = message.get("content", "")

            # Choose the correct content based on system or user messages
            if (
                "Use the following context as your learned knowledge, inside <context></context>"
                in content_sys
            ):
                content = content_sys
            else:
                content = content_message

            # Split content if necessary (e.g., for Nano handling)
            if "\n\n---\n## Attempting to receive Nano:" in content:
                content = content.split("\n\n---\n## Attempting to receive Nano:")[0]

            # Prepare processed messages
            processed_messages = [
                {
                    "role": message["role"],
                    "content": content,
                }
                for message in messages
            ]

            # Remove the system message from `messages` and pass it as top-level
            model_name = body.get("model", "")
            if model_name.startswith("nanogpt2."):
                model_name = model_name[len("nanogpt2.") :]

            payload = {
                "model": model_name,
                "system": system_message,  # Send the system message at the top level
                "messages": processed_messages,  # User/Assistant messages only
                "prompt": content,
            }

            headers = {
                "x-api-key": self.valves.NANO_GPT_API_KEY,
                "Content-Type": "application/json",
            }
            print(f"Using model: {model_name}")  # Log the model name
            print(f"Using Payload: {payload}")

            start_time = time.time()
            r = requests.post(
                url=f"{self.valves.NANO_GPT_API_BASE_URL}/stream-gpt",
                headers=headers,
                json=payload,
                timeout=120,  # Increased timeout
            )
            elapsed_time = time.time() - start_time
            print(f"Request took {elapsed_time} seconds")

            r.raise_for_status()
            print(f"Result: {r}")

            result = r.content.decode("utf-8", errors="replace")
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
                    print(f"Title: {text_response}")
                    return text_response

            # Extract NanoGPT info
            try:
                nano_info = json.loads(parts[1].split("</NanoGPT>")[0])
            except (IndexError, json.JSONDecodeError) as e:
                print(f"Error parsing NanoGPT info: {e}")
                return "Error: Failed to parse NanoGPT info."

            cost = nano_info.get("nanoCost", "0")

            # Fetch balance and deposit address
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
                print(f"Error fetching balance: {rbo.status_code} - {rbo.text}")

            # After fetching the balance and deposit address
            try:
                balance_val = float(balance)
                cost_val = float(cost)
            except ValueError:
                print(f"Invalid balance or cost values: balance={balance}, cost={cost}")
                return "Error: Invalid balance or cost value."

            if balance_val < 5:
                info = "warning"
                contentban = f"🪙Balance: {balance} Nano 🪙.\n\n Use the Recive Nano Action Button to get deposit address and qr code."
                await __event_emitter__(
                    {
                        "type": "confirmation",
                        "data": {
                            "title": "⚠️ Warning Nano Balance Low ⚠️",
                            "message": contentban,
                        },
                    }
                )

            else:
                info = "success"
                contentban = f"🪙Balance: {balance} Nano 🪙"

            if cost_val > 1:
                await __event_emitter__(
                    {
                        "type": "confirmation",
                        "data": {
                            "title": "⚠️ Warning Nano Message Cost High ⚠️",
                            "message": f"Last message cost was 🪙 {cost} Nano 🪙.\n\n Please start a new Chat to lower costs.",
                        },
                    }
                )
            else:
                pass

            # Construct the banner data
            banners_data = [
                {
                    "id": "nanobalancebanner",
                    "type": info,
                    "title": "string",
                    "content": contentban,
                    "dismissible": False,
                    "timestamp": int(time.time()),
                }
            ]

            config = get_config()
            config_ui = config.get("ui", {})
            config_ui["banners"] = banners_data
            config["ui"] = config_ui
            save_config(config)

            print("Banner Set")

            return text_response

        except requests.exceptions.Timeout:
            print("Request to Nano GPT API timed out.")
            return "Error: The request timed out. Please try again later."
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred at {current_time}: {http_err}")
            print(f"Response text at {current_time}: {r.text}")
            return f"Please try a different model. If {model_name} is a newer AI model it could be overloaded (504 Server Error) or down (404 Server Error). You may try {model_name} again after some time. Error Details: Received HTTP status {r.status_code} from the API."
        except Exception as e:
            print(f"Unexpected error in pipe method: {e}")
            return f"Error: {str(e)}"
