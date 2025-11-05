import requests
import zipfile
import os
import time
from shutil import rmtree

SUBROOT      = os.path.dirname(os.path.dirname(__file__)) # tht
VMT_DIR_PATH = os.path.join(SUBROOT, 'vm-templates')

class retrive:
    def __init__(self, source):
        self.source  = source

        self.dest    = VMT_DIR_PATH
        self.zippath = os.path.join(VMT_DIR_PATH, f"{self.source.repo}.zip")
        self.unzipped_name = os.path.join(VMT_DIR_PATH, f"{self.source.repo}")
    

    @property
    def cloneulr(self) -> str:
        return f"https://github.com/{self.source.owner}/{self.source.repo}/archive/refs/heads/{self.source.branch}.zip"
    

    def download(self):
        url = self.cloneulr

        if self.source.token:
            headers = {}
            headers['Authorization'] = f'token {self.source.token}'
            response = requests.get(url, headers=headers, stream=True)
        else:
            response = requests.get(url, stream=True)

        self.source.logger.log("INFO", f"Downloading repository from {url}...")
        try:
            if response.status_code == 200:
                os.makedirs(os.path.dirname(self.zippath), exist_ok=True)
                with open(self.zippath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.source.logger.log("SUCCESS", f"Download successful! File saved as {self.zippath}")
            else:
                raise Exception("Download failed.")
        except:
            self.source.logger.log("ERROR", f"Failed to download repository. Status code: {response.status_code}")
            self.source.logger.log("ERROR", response.text)



    def unzip(self):
        extended_name = f"{self.unzipped_name}-{self.source.branch}"

        self.source.logger.log("INFO", f"Extracting {extended_name}.zip")
        with zipfile.ZipFile(self.zippath, 'r') as zip_ref:
            zip_ref.extractall(self.dest)
        self.source.logger.log("SUCCESS", f"Extraction of {extended_name}.zip completed!")
        os.remove(self.zippath)

        self.source.logger.log("WARNING", f'Clearing old Files in {self.dest}')
        if os.path.exists(self.unzipped_name):
            rmtree(self.unzipped_name)
        os.rename(extended_name, self.unzipped_name)


    def update(self):
        try:
            self.download()
            self.unzip()
        except Exception as e:
            self.source.logger.log("ERROR", f"Error during update: {e}")