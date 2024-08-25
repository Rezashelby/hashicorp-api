import os
from dotenv import load_dotenv

load_dotenv()

from Nomad.nomad import NomadApi  
def main():
    token = os.getenv('NOMAD_API_TOKEN')
    url = os.getenv('NOMAD_API_URL')
 
    # Initialize the NomadApi class with the parameters
    nomad_api = NomadApi(
        token=token,
        url=url,
 
    )

 
    namespace = "default"
    try:
        job_info = nomad_api.getJobInfo(namespace)
        print("Job Info:", job_info)
    except Exception as e:
        print(f"Failed to fetch job info: {e}")

if __name__ == "__main__":
    main()
