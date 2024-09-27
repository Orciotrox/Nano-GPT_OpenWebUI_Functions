"""
title: Nano GPT Image Gen
author: Elliott Groves
version: 1.0
date: 2024-09-24
description: Nano GPT Image Gen action button for openwebui.
author_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
funding_url: https://github.com/Orciotrox/Nano-GPT.com_OpenWebUI
nano_address: nano_1pkmodta8fg8ti39pr1doe1mjbwo8cu3c9mt5u38d73d5t57d9nmgmnheifk
icon_url: data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48IS0tIFVwbG9hZGVkIHRvOiBTVkcgUmVwbywgd3d3LnN2Z3JlcG8uY29tLCBHZW5lcmF0b3I6IFNWRyBSZXBvIE1peGVyIFRvb2xzIC0tPgo8c3ZnIHdpZHRoPSI4MDBweCIgaGVpZ2h0PSI4MDBweCIgdmlld0JveD0iMCAwIDMyIDMyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPg0KPHBhdGggZD0iTTI1LjYgMEg2LjRDMi44NjUzOCAwIDAgMi44NjUzOCAwIDYuNFYyNS42QzAgMjkuMTM0NiAyLjg2NTM4IDMyIDYuNCAzMkgyNS42QzI5LjEzNDYgMzIgMzIgMjkuMTM0NiAzMiAyNS42VjYuNEMzMiAyLjg2NTM4IDI5LjEzNDYgMCAyNS42IDBaIiBmaWxsPSJ1cmwoI3BhaW50MF9saW5lYXJfMTAzXzE3ODkpIi8+DQo8cGF0aCBkPSJNNS45NTc3IDI0Ljg4NDVDNS40MjU3OCAyNS45NDgzIDYuMTk5MzcgMjcuMiA3LjM4ODc4IDI3LjJIMTguMjExMUMxOS40MDA1IDI3LjIgMjAuMTc0MSAyNS45NDgzIDE5LjY0MjIgMjQuODg0NUwxNC4yMzEgMTQuMDYyMkMxMy42NDE0IDEyLjg4MjkgMTEuOTU4NSAxMi44ODI5IDExLjM2ODggMTQuMDYyMkw1Ljk1NzcgMjQuODg0NVoiIGZpbGw9IndoaXRlIi8+DQo8cGF0aCBkPSJNMTUuNTU3NyAyNC44ODQ1QzE1LjAyNTggMjUuOTQ4MyAxNS43OTk0IDI3LjIgMTYuOTg4OCAyNy4ySDI0LjYxMTFDMjUuODAwNSAyNy4yIDI2LjU3NDEgMjUuOTQ4MyAyNi4wNDIyIDI0Ljg4NDVMMjIuMjMxIDE3LjI2MjJDMjEuNjQxNCAxNi4wODI5IDE5Ljk1ODUgMTYuMDgyOSAxOS4zNjg4IDE3LjI2MjJMMTUuNTU3NyAyNC44ODQ1WiIgZmlsbD0id2hpdGUiIGZpbGwtb3BhY2l0eT0iMC42Ii8+DQo8cGF0aCBkPSJNMjQuMDAwMiAxMS4yQzI1Ljc2NzUgMTEuMiAyNy4yMDAyIDkuNzY3MjYgMjcuMjAwMiA3Ljk5OTk1QzI3LjIwMDIgNi4yMzI2NCAyNS43Njc1IDQuNzk5OTUgMjQuMDAwMiA0Ljc5OTk1QzIyLjIzMjkgNC43OTk5NSAyMC44MDAyIDYuMjMyNjQgMjAuODAwMiA3Ljk5OTk1QzIwLjgwMDIgOS43NjcyNiAyMi4yMzI5IDExLjIgMjQuMDAwMiAxMS4yWiIgZmlsbD0id2hpdGUiLz4NCjxkZWZzPg0KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDBfbGluZWFyXzEwM18xNzg5IiB4MT0iMTYiIHkxPSIwIiB4Mj0iMTYiIHkyPSIzMiIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPg0KPHN0b3Agc3RvcC1jb2xvcj0iIzAwRTY3NiIvPg0KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMDBDODUzIi8+DQo8L2xpbmVhckdyYWRpZW50Pg0KPC9kZWZzPg0KPC9zdmc+
"""
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
import asyncio


class ImageModel(BaseModel):
    id: str
    name: str
    description: str
    cost: dict
    maxImages: int
    resolutions: list
    engine: str


class Action:
    class Valves(BaseModel):
        NANO_GPT_API_KEY: str = Field(
            default="Your Nano GPT API Key",
            description="API key for authenticating requests to the Nano GPT API.",
        )
        NAME_PREFIX: str = Field(
            default="NanoGPT-Image/",
            description="Prefix to be added before model names.",
        )
        NANO_GPT_API_BASE_URL: str = Field(
            default="https://nano-gpt.com/api",
            description="Base URL for accessing Nano GPT API endpoints.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.models = []

    async def fetch_models(self) -> List[ImageModel]:
        try:
            headers = {
                "Authorization": f"Bearer {self.valves.NANO_GPT_API_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.get(
                f"{self.valves.NANO_GPT_API_BASE_URL}/models", headers=headers
            )
            response.raise_for_status()

            models = response.json().get("models", {}).get("image", {})
            if not models:
                return []

            return [
                ImageModel(
                    id=model_info.get("model"),
                    name=model_info.get("name", model_key),
                    description=model_info.get("description", ""),
                    cost=model_info.get("cost", {}),
                    maxImages=model_info.get("maxImages", 1),
                    resolutions=[res["value"] for res in model_info.get("resolutions", [])],
                    engine=model_info.get("engine", ""),
                )
                for model_key, model_info in models.items()
            ]

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

    async def action(self, body: dict, __user__=None, __event_emitter__=None, __event_call__=None) -> Optional[dict]:
        print(f"action: {__name__}")

        # Fetch available models
        models = await self.fetch_models()
        if not models:
            print("No models available for selection.")
            return

        # Display model selection options
        selection_text = "\n\n".join([f"{i + 1}. {model.name} - {model.description}" for i, model in enumerate(models)])

        selection_data = {
            "type": "input",
            "data": {
                "title": "Nano GPT Image Models",
                "message": f"Input the number of the model you would like to use:\n\n{selection_text}",
                "placeholder": selection_text,
            },
        }

        try:
            # Get user-selected model
            selected_index = await __event_call__(selection_data)
            if not selected_index or not (1 <= int(selected_index) <= len(models)):
                print("Invalid model selection.")
                return

            selected_model = models[int(selected_index) - 1]
            print(f"Selected Model: {selected_model.name}")

            # Get image width
            width_data = {
                "type": "input",
                "data": {
                    "title": "Image Width",
                    "message": "Enter the width of the image (default is 1024):",
                    "placeholder": "1024",
                },
            }
            width = await __event_call__(width_data)
            width = int(width) if width else 1024

            # Get image height
            height_data = {
                "type": "input",
                "data": {
                    "title": "Image Height",
                    "message": "Enter the height of the image (default is 1024):",
                    "placeholder": "1024",
                },
            }
            height = await __event_call__(height_data)
            height = int(height) if height else 1024

            # Get prompt for image generation
            prompt_data = {
                "type": "input",
                "data": {
                    "title": "Image Prompt",
                    "message": "Enter the prompt for image generation:",
                    "placeholder": "A beautiful landscape",
                },
            }
            image_prompt = await __event_call__(prompt_data)

            # Generate the image
            response_data = self.generate_image(image_prompt, selected_model.id, width, height)
            if not response_data or "data" not in response_data or not response_data["data"]:
                raise Exception("No image data in the response")

            image_data = response_data["data"][0].get("b64_json")
            if not isinstance(image_data, str):
                raise Exception("Invalid image data format")

            content = f"![Generated Image](data:image/png;base64,{image_data})\n\n"

            await __event_emitter__({"type": "message", "data": {"content": content}})
            await __event_emitter__({"type": "image", "data": {"content": image_data}})

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": "Image Generated", "done": True}})

        except Exception as e:
            error_message = f"Error processing image: {e}"
            print(error_message)
            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": "Error Generating Image", "done": True}})
                await __event_emitter__({"type": "message", "data": {"content": error_message}})

    def generate_image(self, prompt, model_id, width, height):
        data = {
            "prompt": prompt,
            "model": model_id,
            "width": width,
            "height": height,
        }
        headers = {
            "x-api-key": self.valves.NANO_GPT_API_KEY,
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.valves.NANO_GPT_API_BASE_URL}/generate-image", headers=headers, json=data
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error Content: {response.text}")
            return None
