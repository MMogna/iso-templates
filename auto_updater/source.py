import os 
import sys
import json

from tht.sha import sha
from tht.retrive import retrive

class source:
    def __init__(self, ghs:dict, logger):

        self.ghs = ghs

        self.owner  = self.getGHSetting(value='owner')
        self.repo   = self.getGHSetting(value='repo')
        self.branch = self.getGHSetting(value='branch')
        self.token  = self.getGHSetting(value='token')

        self.sha     = sha(source=self)
        self.retrive = retrive(source=self)

        self.logger = logger

    def getGHSetting(self, value:str) -> str:
        source = self.ghs
        if source is None:
            return None
        else: 
            out = source.get(value)
            return out
    
    @property    
    def needsUpdate(self) -> bool:
        if self.ghs is None:
            return False
        
        local = self.sha.local
        remote = self.sha.remote

        if local == remote:
            if not os.path.exists(self.retrive.unzipped_name):
                self.logger.log("ERROR", "Templates Files are missing, retriving remote repository anyway")
                return True
            return False
        else:
            with open(self.sha.localpath, 'w') as f:
                f.write(remote)
            return True