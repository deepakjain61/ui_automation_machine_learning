
import os
import glob
import shutil

def file_cleanup(path):
    if os.path.exists(path):
        shutil.rmtree(path)
