import os.path

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

import yaml
import tkinter as tk
import tkinter.filedialog as filedialog
from yaml.loader import SafeLoader

# Step 1: Select file using GUI

# Initialize the GUI window
Tk = tk.Tk()
Tk.title('KI OCR Project Build')
Tk.geometry('640x480')

files = filedialog.askopenfilenames(parent=Tk, title='Choose files for processing')
print(files)

# Initialize frames for GUI, starting with the menu frame
menuFrame = tk.Frame(Tk, bg='gray80')
menuFrame.grid(row=0, column=0, columnspan=2)
menuFrameFileBtn = tk.Button(menuFrame, text='Open')
menuFrameFileBtn.grid(row=0,column=0)
menuFrameFileBtn = tk.Button(menuFrame, text='Config')
menuFrameFileBtn.grid(row=0,column=1)
# Initialize the components for the listbox component
listFrame = tk.Frame(Tk)
listFrame.grid(row=1, column=0)
listFrameScrollbar = tk.Scrollbar(listFrame, orient=tk.VERTICAL)
listFrameScrollbar.grid(row=0, column=1)
listFrameList = tk.Listbox(listFrame, yscrollcommand=listFrameScrollbar.set, selectmode=tk.MULTIPLE)
listFrameList.grid(row=0, column=0)
# Initialize action frame component
actionFrame = tk.Frame(Tk)
actionFrame.grid(row=1, column=1)
actionFrameBtn = tk.Button(actionFrame, text='Process')
actionFrameBtn.grid(row=0, column=0, pady=2, padx=2)

Tk.rowconfigure(1, weight=1)
Tk.columnconfigure(0, weight=1)
Tk.columnconfigure(1, weight=1)

def listFrameInit(window):
    print("List frame init")


for i in range(len(files)):
    fileName = os.path.basename(files[i])
    print(fileName)
    listFrameList.insert(tk.END, fileName)
    # msg = tk.Label(Tk, text=fileName)
    # msg.grid(row=i, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=2, padx=2)
    # btn = tk.Button(Tk, text='Process')
    # btn.grid(row=i, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), pady=2, padx=2)
    # Tk.rowconfigure(i, weight=1)
    # btn.pack()

listFrameScrollbar.config(command=listFrameList.yview)

Tk.mainloop()

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

# Iterate through the selected files
for file in files:
    with open(file, 'rb') as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=f)
    result = poller.result()

print("Document contains content: ", result.content)
