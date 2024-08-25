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


def main():

    job_info("default")
    sumbit_job()


if __name__ == "__main__":
    main()
