from zipfile import ZipFile

import pandas as pd
import requests
import xmltodict

xml = '<RequestVeiculo><login>23218039000185</login><senha>285017</senha></RequestVeiculo>'
url = "https://webservice.newrastreamentoonline.com.br/"
headers = {'Content-Type': 'application/xml'}
response = requests.post(url, data=xml, headers=headers).content
with open('./response.zip', 'wb') as zipFile:
    zipFile.write(response)
newzipFile = ZipFile('response.zip')
files_list = newzipFile.namelist()
file_content = newzipFile.open(files_list[0]).read()
xmlDict = xmltodict.parse(file_content)
df = pd.DataFrame.from_dict(xmlDict, orient='index')
df3 = pd.DataFrame.from_dict(xmlDict['ResponseVeiculo']['Veiculo'])
