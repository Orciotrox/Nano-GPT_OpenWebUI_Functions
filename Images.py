from pydantic import BaseModel, Field
from typing import Optional, List
import requests
import json
import base64


class OpenAI:
    def __init__(self, valves):
        self.base_url = valves.OPENAI_API_BASE_URL
        self.api_key = valves.OPENAI_API_KEY

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def models(self) -> List[dict]:
        try:
            response = requests.get(
                f"{self.base_url}/imagemodels", headers=self.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                models = data["data"]
                return [{"id": model["id"], "name": model["id"]} for model in models]
            else:
                print("Unexpected response structure.")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching models: {e}")
            return []

    def generate_image(
        self, prompt: str, model_id: str, size: str, num_images: int
    ) -> dict:
        payload = {"prompt": prompt, "model": model_id, "size": size, "n": num_images}
        try:
            response = requests.post(
                f"{self.base_url}/generateImage",
                json=payload,
                headers=self.get_headers(),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error generating image: {e}")
            return {}


class Action:
    class Valves(BaseModel):
        OPENAI_API_BASE_URL: str = Field(
            default="",
            description="The base URL for Node RED API and image generation",
        )
        OPENAI_API_KEY: str = Field(
            default="",
            description="Your Nano GPT API key for accessing the API",
        )
        IMAGE_SIZE: str = Field(
            default="1024x1024", description="The size of generated images"
        )
        NUM_IMAGES: int = Field(
            default=1, description="The number of images to generate"
        )

    class UserValves(BaseModel):
        show_status: bool = Field(
            default=True, description="Show status of the action."
        )

    def __init__(self):
        self.valves = self.Valves()
        self.client = OpenAI(self.valves)

    def fetch_models(self) -> List[dict]:
        return self.client.models()

    def choose_model(self, models: List[dict]) -> Optional[dict]:
        return models[0] if models else None

    def process_linebreaks(self, data):
        if isinstance(data, str):
            return data.replace("LINEBREAKHERE", "\n")
        elif isinstance(data, dict):
            return {k: self.process_linebreaks(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_linebreaks(item) for item in data]
        return data

    async def action(
        self, body: dict, __user__=None, __event_emitter__=None, __event_call__=None
    ) -> Optional[dict]:
        print(f"action:{__name__}")

        user_valves = __user__.get("valves")
        if not user_valves:
            user_valves = self.UserValves()

        models = self.fetch_models()
        if not models:
            print("No models available for selection.")
            return

        selected_model = self.choose_model(models)
        if not selected_model:
            print("No model selected or available.")
            return

        print(f"Selected Model: {selected_model['name']}")

        last_user_message = body["messages"][-1]["content"]

        try:
            if user_valves.show_status:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Generating Image",
                            "done": False,
                        },
                    }
                )

            response_data = self.client.generate_image(
                prompt=last_user_message,
                model_id=selected_model["id"],
                size=self.valves.IMAGE_SIZE,
                num_images=self.valves.NUM_IMAGES,
            )

            # Process LINEBREAKHERE in response_data
            response_data = self.process_linebreaks(response_data)

            print(f"API Response: {response_data}")

            if not response_data or "imageData" not in response_data:
                raise Exception("No image data in the response")

            image_data = response_data["imageData"].split(",")[1]

            content = f"![Generated Image](data:image/png;base64,{image_data})\n\n"

            # Add the prompt content without the "prompt:" label
            if "prompt" in response_data:
                content += f"{response_data['prompt']}\n\n"

            # Add other information, excluding specific fields
            excluded_fields = {"prompt", "model_id", "size", "num_image", "imageData"}
            for key, value in response_data.items():
                if key not in excluded_fields:
                    content += f"{value}\n"

            if user_valves.show_status:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Image Generated",
                            "done": True,
                        },
                    }
                )

            await __event_emitter__(
                {
                    "type": "message",
                    "data": {"content": content},
                }
            )

            # Emit the image separately as well
            await __event_emitter__(
                {
                    "type": "image",
                    "data": {"content": image_data},
                }
            )

        except Exception as e:
            error_message = f"Error processing image: {str(e)}"
            print(error_message)
            if user_valves.show_status:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Error Generating Image",
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

        return None
