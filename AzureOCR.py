from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import yaml
from yaml.loader import SafeLoader

# Step 1: Select file for processing
print("Please input path of file...")
filePath = input("Path: ")
print(filePath)

# TODO, have a file selection dialog

# Step 2: Extract Azure credentials securely from remote config file
with open ('config.yaml', 'r') as f:
    data = yaml.load(f, Loader=SafeLoader)
    azure_config = data['azure']

SUBSCRIPTION_KEY = azure_config['SUBSCRIPTION_KEY']
ENDPOINT = azure_config['ENDPOINT']
azure_vision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

