"""
title: Nano GPT Revice Nano and info
author: Elliott Groves
version: 1.0.2
date: 2024-10-10
description: Nano GPT recive Nano balance button for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
nano_donation_address: nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk
icon_url: data:image/svg+xml;base64, IDxzdmcgIHZlcnNpb249IjEuMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiAgd2lkdGg9IjMwMC4wMDAwMDBwdCIgaGVpZ2h0PSIzMDAuMDAwMDAwcHQiIHZpZXdCb3g9IjAgMCAzMDAuMDAwMDAwIDMwMC4wMDAwMDAiICBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCBtZWV0Ij4gIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuMDAwMDAwLDMwMC4wMDAwMDApIHNjYWxlKDAuMTAwMDAwLC0wLjEwMDAwMCkiIGZpbGw9IiM5YjliOWIiIHN0cm9rZT0ibm9uZSI+IDxwYXRoIGQ9Ik0xMzE1IDI5NDkgYy01NjEgLTc3IC0xMDE4IC00NTAgLTEyMDQgLTk4MSAtMTAwIC0yODcgLTEwMiAtNjMwIC02IC05MjQgMzMgLTEwMCAxMDMgLTI0OSAxNTMgLTMyOCAxMTMgLTE3NiAyODMgLTM0NiA0NTggLTQ1OCAxMzcgLTg4IDM2NiAtMTc0IDUzOSAtMjAzIDEzMSAtMjIgMzQ5IC0yMiA0ODAgMCA2MTIgMTAzIDEwOTUgNTg1IDEyMDEgMTIwMCAyMiAxMjkgMjIgMzQ3IDAgNDc4IC0yNiAxNTUgLTU2IDIwOCAtMTI4IDIyNyAtNTQgMTUgLTEwOSAtMiAtMTQ3IC00NSAtNDAgLTQ1IC00NiAtODcgLTI2IC0xNjEgMjMgLTgxIDMxIC0zMzEgMTUgLTQzMiAtNzYgLTQ3NyAtNDE2IC04NDUgLTg4OSAtOTY1IC03NCAtMTkgLTExMyAtMjIgLTI3MSAtMjEgLTE2NyAwIC0xOTQgMyAtMjgzIDI3IC0yODAgNzUgLTUyOCAyNTAgLTY3OSA0NzcgLTE0MCAyMTIgLTE5OSA0MDYgLTE5OSA2NTcgMCA0NTggMjUwIDg1NiA2NjIgMTA1MyAyODYgMTM2IDYzNyAxNTEgOTIwIDQwIDg1IC0zNCAxNTIgLTIyIDE5OCAzNiA0MiA1NCAzNyAxNDcgLTEyIDE5MiAtMzIgMzAgLTE5MiA4NyAtMzE5IDExMyAtMTE5IDI0IC0zNTQgMzMgLTQ2MyAxOHoiLz4gPHBhdGggZD0iTTI4MjIgMjgwOCBjLTE4IC0xMyAtMTQ5IC0xNTAgLTI5MSAtMzA0IGwtMjU5IC0yODIgLTg4IDg5IGMtMTIzIDEyNCAtMTYzIDEzOSAtMjI3IDg5IC0zNCAtMjcgLTQ0IC03OCAtMjQgLTExNiAyNiAtNDggMjc5IC0yOTMgMzEyIC0zMDIgMzEgLTkgNTggLTQgODUgMTMgMzMgMjEgNjMxIDY3NyA2NDEgNzAyIDEyIDMxIC0zIDgyIC0zMCAxMDcgLTMyIDI5IC04MiAzMSAtMTE5IDR6Ii8+IDxwYXRoIGQ9Ik0xNzA1IDI0OTYgYy00MSAtMTggLTEwNyAtOTQgLTEyNCAtMTQyIC03IC0yMSAtMzUgLTkzIC02MSAtMTU5IC0yNiAtNjYgLTUwIC0xMjkgLTU0IC0xNDAgLTYgLTE1IC0yMCAxMSAtNjEgMTE1IC0yOSA3NCAtNjAgMTUzIC02OSAxNzUgLTkgMjMgLTMzIDU4IC01NCA3OSAtNzMgNzYgLTE0NiA4MyAtMjAxIDIxIC02NyAtNzcgLTU4IC0xMzUgNzcgLTQ4NiBsMTA5IC0yODQgLTIwMSAtNSBjLTEyOSAtMyAtMjA4IC05IC0yMjIgLTE3IC01NCAtMzEgLTU0IC03MSAtMSAtMTAwIDI2IC0xNSA2NiAtMTggMjI1IC0yMSAxMDUgLTIgMTkyIC02IDE5MiAtOCAwIC0yIC0xMiAtMzMgLTI2IC02OSBsLTI2IC02NSAtMTQ3IDAgYy0xMjMgMCAtMTUzIC0zIC0xODkgLTIwIC0zNyAtMTcgLTQzIC0yMyAtNDAgLTQ2IDIgLTE1IDE1IC0zNiAzMSAtNDggMjUgLTE4IDQ1IC0yMSAxNTggLTI1IDcxIC0xIDEyOSAtNiAxMjkgLTkgMCAtMyAtMzYgLTk4IC03OSAtMjExIC04OCAtMjMxIC05NyAtMjY3IC04MCAtMzM0IDM4IC0xNTQgMjA1IC0xMzYgMjg4IDMyIDE1IDMxIDYxIDE0MiAxMDEgMjQ4IDQxIDEwNiA3NyAxOTAgODEgMTg3IDQgLTIgMTQgLTI1IDIzIC01MiA5IC0yNiA1MCAtMTMzIDkyIC0yMzggOTYgLTI0NiAxNDMgLTMwNCAyNDMgLTMwNCA0OSAwIDk1IDM1IDExMiA4NyAyMSA2NiA1IDEzNiAtODQgMzY4IGwtODYgMjIwIDEyMiA1IGMxMjcgNSAxNzIgMTggMTgyIDUxIDE1IDQ3IC0zOSA3OSAtMTMwIDc5IC0yOSAwIC05MiAzIC0xNDIgNiBsLTg5IDcgLTI2IDY4IC0yNiA2OSAxNTQgMCBjMTY3IDAgMjEzIDEwIDIzNCA1MCAxMCAxOCA4IDI2IC0xMCA0NiAtMjkgMzAgLTkyIDQxIC0yNTAgNDQgLTY5IDEgLTEyNiAzIC0xMjggNSAtMiAxIDQ3IDEzMyAxMDkgMjkxIDkzIDI0MiAxMTIgMzAxIDExNiAzNTkgNiA4NiAtMTEgMTM2IC01OSAxNjUgLTM4IDIzIC03MCAyNSAtMTEzIDZ6Ii8+IDwvZz4gPC9zdmc+IA==
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

            if not response_data:
                raise Exception("No data in the response")

            headers = {
                "x-api-key": self.valves.NANO_GPT_API_KEY,
                "Content-Type": "application/json",
            }

            # Check balance and deposit address
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

            balance_message = f"\n- **🪙 Balance 🪙:** {balance} Nano"
            deposit_message = f"\n- **🏛️ Nano Deposit Address 🏛️:** `{resultdep}`"

            # Determine the message based on received blocks
            if response_data.get("receivedBlocks"):
                message = "Successfully received Nano"
                # message = "\n- **📌 Response 📌:** Successfully received Nano"
            elif not response_data.get("receivedBlocks") and not response_data.get(
                "failedReceivableBlocks"
            ):
                message = "No Nano to receive"
                # message = "\n- **📌 Response 📌:** No Nano to receive"
            else:
                message = "Error Unexpected response"
                # message = "\n- **📌 Response 📌:** Error Unexpected response"

            urlqr = f"https://api.qrserver.com/v1/create-qr-code/?data={resultdep}&size=300x300"
            table = f"---\n ## Attempting to receive Nano:\n>``` 📌 Response 📌\n{message}\n>``` \n>``` 🪙 Balance 🪙\n{balance} Nano\n>``` \n>``` 🏛️ Nano Deposit Address 🏛️\n{resultdep}\n>```\n 🏛️ Nano Deposit QR Code 🏛️\n![🏛️ Nano Deposit QR Code 🏛️]({urlqr})\n---"
            message = table

            # Emit status messages back to the UI
            await __event_emitter__(
                {
                    "type": "message",
                    "data": {"content": message},
                }
            )

        except Exception as e:
            error_message = f"---\n ## Error receiving Nano:\n>``` {str(e)}\n>```Try resetting the API Key for Nano-gpt.com in openwebui.\n---"
            print(error_message)
            await __event_emitter__(
                {
                    "type": "message",
                    "data": {"content": message},
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
            return response.json()

        except requests.RequestException as e:
            print(f"Error receiving Nano: {e}")
            return None
