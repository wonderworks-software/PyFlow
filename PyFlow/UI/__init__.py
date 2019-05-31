import sys
import os
fileDir = os.path.dirname(__file__)
fileDir = fileDir.replace("\\", "/")
sys.path.append(fileDir)
RESOURCES_DIR = fileDir + "/resources"
