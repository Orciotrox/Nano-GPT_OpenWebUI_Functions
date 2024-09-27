"""
title: Nano GPT Revice Nano
author: Elliott Groves
version: 1.0
date: 2024-09-24
description: Nano GPT recive Nano balance button for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
nano_address: nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk
"""
from pydantic import BaseModel, Field
from typing import Optional
import requests
import asyncio

class Action:
    class Valves(BaseModel):
        NANO_GPT_API_KEY: str = Field(
            default="Your Nano GPT API Key",
            description="API key for authenticating requests to the Nano GPT API.",
        )
        NANO_GPT_API_BASE_URL: str = Field(
            default="https://nano-gpt.com/api",
            description="Base URL for accessing Nano GPT API endpoints.",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        print("action: Receive Nano")

        try:
            # Call the receive Nano method
            response_data = self.receive_nano()

            # Check the response and determine which message to send
            if response_data is None:
                raise Exception("No data in the response")

            # If 'receivedBlocks' contains items, Nano was successfully received
            if response_data.get('receivedBlocks'):
                success_message = "Successfully received Nano"
                print(success_message)
                content = f"{success_message}:\n\n{response_data}\n\n"

            # If both 'receivedBlocks' and 'failedReceivableBlocks' are empty, there's no Nano to receive
            elif not response_data.get('receivedBlocks') and not response_data.get('failedReceivableBlocks'):
                no_nano_message = "No Nano to receive"
                print(no_nano_message)
                content = f"{no_nano_message}\n\n"

            # Emit the content message back to the UI
            await __event_emitter__(
                {
                    "type": "message",
                    "data": {"content": content},
                }
            )

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Nano Receive Process Completed",
                        "done": True,
                    },
                }
            )

        except Exception as e:
            error_message = f"Error receiving Nano: {str(e)}"
            print(error_message)
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Error Receiving Nano",
                            "done": True,
                        },
                    }
                )
                await __event_emitter__(
                    {
                        "type": "message",
                        "data": {"content": error_message},
                    }
                )

    def receive_nano(self):
        # Function to interact with the Nano GPT API and receive Nano
        url = f"{self.valves.NANO_GPT_API_BASE_URL}/receive-nano"
        headers = {
            "x-api-key": self.valves.NANO_GPT_API_KEY,
            "Content-Type": "application/json",
        }

        try:
            print("Attempting to receive Nano...")
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            print(f"Response Status Code: {response.status_code}")
            return response.json()

        except requests.RequestException as e:
            print(f"Error receiving Nano: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            return None
