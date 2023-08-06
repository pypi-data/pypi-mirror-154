import io
import json
import os
import sys
import json
from argparse import Namespace
import os

from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

class SafeKeep:
    def __init__(self, excludeFolders = ['venv','.idea',".git","__pycache__","output","temp"]):
        baseDir = os.path.dirname(os.path.realpath(__file__))
        folderName = baseDir.split(os.sep)[-1]
        oldfolderName=folderName
        if folderName.split(".")[-1].isdigit():
            v = int(baseDir.split(".")[-1])+1
            folderName = folderName.split(".")[:-1][0]+ ".%d" %v
            fileName = folderName + ".zip"
        else:
            fileName = baseDir.split(os.sep)[-1].split() + datetime.now().strftime("%d-%m-%Y.%H:%M:%S") + ".zip"

        homeDir = baseDir.replace(folderName,"")

        # password = input("Password please:")
        try:
            authcookie = Office365('https://myrp.sharepoint.com', username='morgan_heijdemann@rp.edu.sg', password='xxx').GetCookies()
        except Exception as e:
            if isinstance(e.args, tuple):
                e = "\n".join(e.args)
            sys.exit(str(e))

        print("baseDir   :", baseDir)
        print("fileName  :", fileName)
        print("cookie    :", authcookie)
        print("homeDir   :", homeDir)
        print("folderName:", folderName)

        site = Site('https://myrp.sharepoint.com/sites/ProjectImplementation/', version=Version.v365, authcookie=authcookie)
        folder = site.Folder('Shared Documents/General/LSH_PO_read')

        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w", compression=ZIP_DEFLATED) as zip_file:
            for folderName, dirs, filenames in os.walk(baseDir,topdown=True):
                [dirs.remove(d) for d in list(dirs) if d in excludeFolders]
                if "venv" in folderName:
                    continue
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    print(filePath, os.path.basename(os.path.join(folderName, filename)))
                    zip_file.writestr(filePath.replace(homeDir,"").replace(homeDir,"").replace(oldfolderName,folderName), os.path.basename(os.path.join(folderName, filename)))

        folder.upload_file(zip_buffer.getvalue(), fileName)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    file = "config.json"

    def __init__(self):
        if not os.path.isfile(self.file):
            return

        with open(self.file, "r") as f:
            self.cfg = json.loads(f.read(), object_hook=lambda d: Namespace(**d))

    def write(self):
        with open(self.file, 'w') as f:
            json.dump(self.cfg, fp=f, default=lambda o: o.__dict__, indent=2)

    def __getattr__(self, name):
        if name in self.cfg:
            return getattr(self.cfg, name)
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key == "cfg":
            self.__dict__[key] = value
        else:
            self.cfg.__dict__[key] = value

def drawText(frame, text, pos, size=0.8, shadow=0):
    if shadow:
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size, (0, 0, 0), 1, cv2.LINE_AA)

    return frame
cfg = Config()