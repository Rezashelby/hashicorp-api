# Nomad/nomad.py
import requests


class NomadApi:
    def __init__(self, token, url):
        self.token = token
        self.url = url

    def getJobInfo(self, namespace):
        try:
            response = requests.get(
                f"{self.url}/jobs?namespace={namespace}",
                headers={"X-Nomad-Token": self.token},
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error fetching job info: {error}")
            raise

    def submitJob(self, json_data):
        try:
            response = requests.post(
                f"{self.url}/jobs",
                headers={
                    "X-Nomad-Token": self.token,
                    "Content-Type": "application/json",
                },
                json=json_data,
            )

            print("HTTP Status Code:", response.status_code)

            if not response.ok:
                response_body = response.text
                print("Failed job submission:", response_body)
                raise Exception(
                    f"Network response was not ok. Status: {response.status_code}"
                )

            response_data = response.json()
            print("Job submission response:", response_data)
            return response_data

        except requests.exceptions.RequestException as error:
            print("Error submitting job:", error)
            raise

    def stopJob(self, jobName):
        try:
            response = requests.delete(
                f"{self.url}/job/{jobName}?purge=false",
                headers={
                    "X-Nomad-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            if not response.ok:
                raise Exception("Network response was not ok")
            return response.json
        except requests.exceptions.RequestException as error:
            print("Error stopping a job:", error)
            raise

    def deleteJob(self, jobName):
        try:
            response = requests.delete(
                "",
                headers={
                    "X-Nomad-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            if not response.ok:
                raise Exception("Network response was not ok")
            return response.json
        except requests.exceptions.RequestException as error:
            print("Error deleting a job:", error)
            raise

    def ensure_namespaces(self, name):
        try:
            response = requests.get(
                f"{self.url}/namespaces", headers={"X-Nomad-Token": self.token}
            )

            if not response.ok:
                raise Exception(f"Network response was not ok: {response.status_text}")

            response_body = response.text

            try:
                data = response.json()
            except ValueError as parse_error:
                print("Error parsing JSON response:", response_body)
                raise parse_error

            namespaces = [item["Name"] for item in data]
            return name in namespaces

        except requests.exceptions.RequestException as error:
            print("Error fetching namespaces:", error)
            raise error

    def createNamespace(self, name):
        try:
            namespaceConfig = {"Name": name}
            response = requests.post(
                f"{self.url}/namespace/{name}",
                headers={
                    "X-Nomad-Token": self.token,
                    "Content-Type": "application/json",
                },
                json=namespaceConfig,
            )

            if response.status_code != 200:
                response.raise_for_status()

            if response.text.strip():
                return response.json()
            else:
                print("Warning: Empty response body.")
                return f"namespace {name} has been created"
        except requests.exceptions.RequestException as error:
            print(f"Error creating namespace: {error}")
            raise

    def deleteNamespace(self, name):
        try:
            response = requests.delete(
                f"{self.url}/namespace/{name}",
                headers={
                    "X-Nomad-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            if response.status_code != 200:
                response.raise_for_status()

            if response.text.strip():
                return response.json()
            else:
                print("Warning: Empty response body.")
                return f"namespace {name} has been deleted"
        except requests.exceptions.RequestException as error:
            print(f"Error deleting namespace: {error}")
            raise

    def createAndRegisterNomadVolume(self, volumeId, nomadPayload):
        try:
            response = requests.put(
                f"${self.url}/volume/csi/${volumeId}/create",
                headers={
                    "Content-Type": "application/json",
                    "X-Nomad-Token": self.token,
                },
                json=nomadPayload,
            )
            if response.status_code != 200:
                response.raise_for_status()

            if response.text.strip():
                return response.json()
            else:
                print("Warning: Empty response body.")
                return f"volume {volumeId} has been created"
        except requests.exceptions.RequestException as error:
            print(f"Error creating volume: {error}")
            raise
