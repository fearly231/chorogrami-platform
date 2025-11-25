import httpx
import os


class APIClient:
    def __init__(self, base_url=None):
        if base_url is None:
            # W kontenerze Docker używamy zmiennej środowiskowej BACKEND_URL
            # W developmencie lokalnym domyślnie localhost:8000
            base_url = os.getenv("BACKEND_URL", "http://backend:8000")

        # Upewniamy się, że URL kończy się slashem
        if not base_url.endswith("/"):
            base_url += "/"

        self.client = httpx.Client(base_url=base_url)

    def get(self, path, **kwargs):
        response = self.client.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

    def post(self, path, json=None, **kwargs):
        response = self.client.post(path, json=json, **kwargs)
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Dla błędów 422 (validation errors), zwracamy więcej informacji
            if e.response.status_code == 422:
                try:
                    error_detail = e.response.json()
                    error_msg = "Validation errors:\n"
                    if "detail" in error_detail:
                        for error in error_detail["detail"]:
                            field = error.get("loc", ["unknown"])[-1]
                            msg = error.get("msg", "Invalid value")
                            error_msg += f"- {field}: {msg}\n"
                    raise ValueError(error_msg.strip())
                except (ValueError, KeyError):
                    raise ValueError(f"Validation error: {e.response.text}")
            else:
                raise e
