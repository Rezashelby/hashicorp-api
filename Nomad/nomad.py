# Nomad/nomad.py
import requests

class NomadApi:
    def __init__(self, token, url ):
        self.token = token
        self.url = url
 


    def getJobInfo(self, namespace):
        try:
            response = requests.get(
                f'{self.url}/jobs?namespace={namespace}',
                headers={
                    'X-Nomad-Token': self.token
                }
            )
            response.raise_for_status()  
            return response.json()
        
        except requests.exceptions.RequestException as error:
            print(f'Error fetching job info: {error}')
            raise