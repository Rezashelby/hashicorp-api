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
