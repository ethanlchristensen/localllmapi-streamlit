import json
import requests


class OllamaClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 11434):
        self.host = host
        self.port = port
        self.uri = f"http://{self.host}:{self.port}/api"
        self.system_prompt = ""

    def __get_model_list(self):
        try:
            model_list_uri = f"{self.uri}/tags"
            response = requests.get(url=model_list_uri, timeout=5).json()
            return [model["name"] for model in response["models"]]
        except:
            return []

    def models(self):
        return self.__get_model_list()

    def get_chat_completion(self, model, query):
        chat_completion_uri = f"{self.uri}/chat"
        payload = json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": query}],
                "stream": False,
            }
        )
        response = requests.post(
            url=chat_completion_uri,
            data=payload,
            headers={"Content-Type": "application/json"},
        ).json()
        return response
