import os
import json
from dotenv import load_dotenv

load_dotenv()

from Nomad.nomad import NomadApi

token = os.getenv("NOMAD_API_TOKEN")
url = os.getenv("NOMAD_API_URL")

nomad_api = NomadApi(
    token=token,
    url=url,
)


def job_info(namespace):
    try:
        job_info = nomad_api.getJobInfo(namespace)
        print("Job Info:", job_info)
    except Exception as e:
        print(f"Failed to fetch job info: {e}")


def sumbit_job():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "Nomad", "template", "nomad.json"
    )
    print(json_file_path)
    with open(json_file_path, "r") as file:
        job_data = json.load(file)
    try:
        submit_job = nomad_api.submitJob(job_data)
        print(f"Job submit: {submit_job}")
    except Exception as e:
        print(f"Failed to submit job: {e}")


def create_namespace(namespace):
    try:
        create_namespace = nomad_api.createNamespace(namespace)
        print("create namespace", create_namespace)
    except Exception as e:
        print(f"Failed to create namespace: {e}")


def ensureNamespace(namespace):
    try:
        ensure_namespace = nomad_api.ensure_namespaces(namespace)
        if ensure_namespace:
            print(f"namespace {namespace} is available")
        else:
            print(f"namespace {namespace} is not available")

    except Exception as e:
        print(f"Failed to ensure namespace: {e}")


def main():

    # job_info("default")
    # sumbit_job()
    create_namespace("test2")
    ensureNamespace("test2a")


if __name__ == "__main__":
    main()
