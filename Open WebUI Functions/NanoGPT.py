"""
title: Nano GPT 
author: Elliott Groves
version: 2.0
date: 2024-09-24
description: Nano GPT for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
nano_address: nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk
"""
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
            default="",
            description="API key for authenticating requests to the Nano GPT API.",
        )

    def __init__(self):
        self.type = "direct"
        self.valves = self.Valves()

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
        # Extract system message and user messages
        system_message, messages = pop_system_message(body["messages"])

        processed_messages = []
        for message in messages:
            content = message.get("content", "")

            # Check if the content contains the marker for cost
            if "\n\n🪙 Cost:" in content:
                # Split the content at the marker and keep the part before it
                content = content.split("\n\n🪙 Cost:")[0]

            processed_messages.append(
                {
                    "role": message["role"],
                    "content": content,
                }
            )

        model_name = body["model"]
        if model_name.startswith("nanogpt2."):
            model_name = model_name[len("nanogpt2.") :]

        # Ensure the system_message is coerced to a string
        payload = {
            "model": model_name,
            "messages": processed_messages,
            "prompt": content,
        }

        headers = {
            "x-api-key": self.valves.NANO_GPT_API_KEY,
            "Content-Type": "application/json",
        }
        print(f"pipe:{__name__}")
        print(f"Payload: {payload}")

        # Make the POST request
        r = requests.post(
            url=f"{self.valves.NANO_GPT_API_BASE_URL}/talk-to-gpt",
            json=payload,
            headers=headers,
        )
        result = r.text if r.status_code == 200 else "Error"

        # Split the response to separate the text and NanoGPT info
        parts = result.split("<NanoGPT>")

        # Extract the text response (everything before <NanoGPT>)
        text_response = parts[0].strip()

        # Check if the request is for generating a title
        for message in body.get("messages", []):
            if (
                "Create a concise, 3-5 word phrase with an emoji as a title"
                in message.get("content", "")
            ):
                return text_response

        # Extract the NanoGPT info
        nano_info = json.loads(parts[1].split("</NanoGPT>")[0])
        result2 = f"{text_response}\n\n🪙 Cost: {nano_info['nanoCost']} Nano 🪙\n\n📌 If you like this project and wish to donate a Nano: 📌\n\n🏛️ nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk 🏛️"
        cost = f"{nano_info['nanoCost']}"
        print(f"response:{result2}")

        # Fetch balance and deposit address
        rbo = requests.post(
            url=f"{self.valves.NANO_GPT_API_BASE_URL}/check-nano-balance",
            headers=headers,
        )
        rb = rbo.json()
        balance = rb.get("balance", "Error") if rbo.status_code == 200 else "Error"
        resultdep = (
            rb.get("nanoDepositAddress", "Error") if rbo.status_code == 200 else "Error"
        )

        result3 = (
            f"{result2}\n\n"
            f"🪙 Balance: {balance} Nano 🪙\n\n"
            f"🏛️ Nano Deposit Address: {resultdep} 🏛️\n\n"
            f"🌐 Website: https://nano-gpt.com/ 🌐\n\n"
            f"📌 If you make a deposit and it dosen't add to your balance use the NanoGPTRecive action button below: 📌\n\n🖱️ If you still have issues email support@nano-gpt.com 🖱️"
        )

        # Logic to determine the final response based on balance and cost
        try:
            balance = float(balance)  # Convert balance to float for comparison
            cost = float(cost)  # Convert cost to float for comparison

            if balance < 1:
                return result3
            elif cost > 0.5:
                return result2
            else:
                return text_response
        except ValueError:
            return "Error: Invalid balance or cost value."
