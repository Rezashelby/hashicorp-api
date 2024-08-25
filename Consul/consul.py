# Nomad/nomad.py
import requests


class consul:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def getServices(self):
        try:
            response = requests.get(f"{self.url}/agent/services")
            response.raise_for_status
            return response.json
        except requests.exceptions.RequestException as error:
            print(f"Error fetching job info: {error}")
            raise
