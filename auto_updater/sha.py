import requests
import os 

from auto_updater.source import Source

HEREDIR = os.path.abspath(os.path.dirname(__file__))

class sha:
        def __init__(self, source:Source):
            self.source:Source = source

            self.shadir = os.path.join(HEREDIR, 'sha')
            if not os.path.exists(self.shadir):
                os.makedirs(self.shadir, exist_ok=True)

            self.localpath = os.path.join(self.shadir,  f"{self.source.repo}_sha")
            if not os.path.exists(self.localpath):
                # Create the file
                with open(self.localpath, 'w') as f:
                    f.write("") 

        @property
        def local(self) -> str:
            try:
                with open(self.localpath, 'r') as f:
                    out = f.read()
                return out.strip()
            except FileNotFoundError:
                return None

        
        def redefineLocal(self, sha:str):
            pass
        
        @property
        def remote(self):
            url = self.apiurl

            if self.source.token:
                headers = {}
                headers['Authorization'] = f'token {self.source.token}'
                response = requests.get(url, headers=headers)
            else:
                response = requests.get(url)

            # Check for successful response
            if response.status_code == 200:
                data = response.json()
                out = data.get("sha")
                return out
            else:
                print(f"Failed to retrieve commit data: {response.status_code}")
                print(response.text)
        
        @property
        def apiurl(self) -> str:
            sha_url = f"https://api.github.com/repos/{self.source.owner}/{self.source.repo}/commits/{self.source.branch}"
            return sha_url
        