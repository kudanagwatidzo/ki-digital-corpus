import os.path

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

import yaml
import json
import tkinter as tk
import tkinter.filedialog as filedialog
from yaml.loader import SafeLoader

# Global variables
selectedFiles = []

# Global functions
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

# Extract Azure credentials securely from remote config file
with open('config.yaml', 'r') as f:
    data = yaml.load(f, Loader=SafeLoader)
    azure_config = data['azure']
SUBSCRIPTION_KEY = azure_config['SUBSCRIPTION_KEY']
ENDPOINT = azure_config['ENDPOINT']
azure_vision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))
document_analysis_client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(SUBSCRIPTION_KEY))

def processDocument(file):
    with open(file, 'rb') as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=f)
    result = poller.result()

    line_list = []
    symbol_confidence_data = []
    total_confidence = 0

    for page in result.pages:
        for line_idx, line in enumerate(page.lines):
            line_obj = {
                "page_number": page.page_number,
                "line_number": line_idx,
                "line_content": line.content,
                "line_bounding_box": format_polygon(line.polygon)
            }
            line_list.append(line_obj)
        for word in page.words:
            total_confidence += word.confidence
            symbol_confidence_data.append("\nPage: " + str(page.page_number) + ", Symbol: " + word.content + ", Confidence: " + str(word.confidence))

    report_output = "Average Confidence Level: " + str(total_confidence / len(symbol_confidence_data)) + \
        "\nTotal Number of Symbols: " + str(len(symbol_confidence_data)) + "\n"
    line_list_json = json.dumps(line_list, indent=4)

    outputJson = os.path.splitext(os.path.basename(file))[0] + "_OCR_metadata.json"
    outputReport = os.path.splitext(os.path.basename(file))[0] + "_OCR_report.txt"

    with open(outputJson, "w") as f:
        f.write(line_list_json)
    with open(outputReport, "w", encoding="utf-8") as f:
        f.write(report_output)
        for item in symbol_confidence_data:
            f.write(item)

# Callback functions
def listBoxCallback(event):
    # fileName = os.path.basename(files[i])
    selection = event.widget.curselection()
    for select in selection:
        data = event.widget.get(select)
        selectedFiles.append(data)

def processButtonCallback():
    # Disable the process button once OCR starts
    actionFrameBtn['state'] = 'disabled'
    print(selectedFiles)
    # Iterate through the selected files
    for file in selectedFiles:
        processDocument(file)
        tk.messagebox.showinfo("showinfo", "File Successfully Processed")
    # Re-enable process button once OCR is finished
    actionFrameBtn['state'] = 'active'

def openButtonCallback():
    files = filedialog.askopenfilenames(parent=Tk, title='Choose files for processing')
    for i in range(len(files)):
        fileName = files[i]
        listFrameListBox.insert(tk.END, fileName)

def resetButtonCallback():
    listFrameListBox.delete(0, tk.END)

# Initialize the GUI window
Tk = tk.Tk()
Tk.title('KI OCR Project Build')
Tk.geometry('320x240')

# Initialize frames for GUI, starting with the menu frame
menuFrame = tk.Frame(Tk, bg='gray80')
menuFrame.grid(row=0, column=0, columnspan=2)
menuFrameFileBtn = tk.Button(menuFrame, text='Open', command=openButtonCallback)
menuFrameFileBtn.grid(row=0,column=0)
menuFrameFileBtn = tk.Button(menuFrame, text='Reset', command=resetButtonCallback)
menuFrameFileBtn.grid(row=0,column=1)
# Initialize the components for the listbox component
listFrame = tk.Frame(Tk)
listFrame.grid(row=1, column=0)
listFrameScrollbar = tk.Scrollbar(listFrame, orient=tk.VERTICAL)
listFrameScrollbar.grid(row=0, column=1)
listFrameListBox = tk.Listbox(listFrame, yscrollcommand=listFrameScrollbar.set, selectmode=tk.MULTIPLE)
listFrameListBox.bind("<<ListboxSelect>>", listBoxCallback)
listFrameListBox.grid(row=0, column=0)
listFrameScrollbar.config(command=listFrameListBox.yview)
# Initialize action frame component
actionFrame = tk.Frame(Tk)
actionFrame.grid(row=1, column=1)
actionFrameBtn = tk.Button(actionFrame, text='Process', command=processButtonCallback)
actionFrameBtn.grid(row=0, column=0, pady=2, padx=2)

Tk.rowconfigure(1, weight=1)
Tk.columnconfigure(0, weight=1)
Tk.columnconfigure(1, weight=1)

Tk.mainloop()


# for file in selectedFiles:
    # with open(file, 'rb') as f:
    #    poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=f)
    # # print("Document contains content: ", result.content)
