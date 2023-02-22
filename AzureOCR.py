from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

import yaml
from yaml.loader import SafeLoader

# Step 1: Select file for processing
print("Please input name of file...")
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

# Step 3: Upload document to azure form recognizer
# TODO, replace this with local file selection
# formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"

document_analysis_client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(SUBSCRIPTION_KEY))

with open("Dummy/" + filePath, 'rb') as f:
    poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=f)

result = poller.result()

print("Document contains content: ", result.content)
