import azure.functions as func
import uuid
import os
import shutil
from azure.storage.blob import ContainerClient, BlobServiceClient, BlobClient
from zipfile import ZipFile
import tempfile
import os
import pyzipper

storageAccountConnstr = "DefaultEndpointsProtocol=https;AccountName=passprotectedzipp;AccountKey=UTqYjKJi+b3clcNquLQTIRXKic1+0d5SMlU5BFSfTUfB/IUPzntclRI+GQ9nMHfpW1rE0xetSkHv+AStdDhGWw==;EndpointSuffix=core.windows.net"
container = "input"
destcontainer="output"



#define local temp path, on Azure, the path is recommanded under /home 
local_path = tempfile.gettempdir()
tempPathRoot = os.path.join(local_path, os.urandom(24).hex())
unZipTempPathRoot = '/home/temp'


def main(req=func.HttpRequest) -> func.HttpResponse:
    reqBody = req.get_json()
    fileName = reqBody['fileName']
    zipPass =  reqBody['password']

    #container_client = ContainerClient.from_connection_string(storageAccountConnstr,container)
    blob_service_client = BlobServiceClient.from_connection_string(storageAccountConnstr)
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(fileName)
    des_container_client = blob_service_client.get_container_client(destcontainer)

    #download zip file 
    zipFilePath = tempPathRoot
    with open(zipFilePath, "wb") as my_blob:
       download_stream = blob_client.download_blob()
       my_blob.write(download_stream.readall())

    #unzip to temp folder
    unZipTempPath = unZipTempPathRoot + str(uuid.uuid4())
    #with ZipFile(zipFilePath) as zf:
    with pyzipper.AESZipFile(zipFilePath,
                         compression=pyzipper.ZIP_LZMA) as zf:
        zf.extractall(path=unZipTempPath,pwd=bytes(zipPass,'utf8'))

    #upload all files in temp folder
    for root, dirs, files in os.walk(unZipTempPath):
        for file in files: 
            filePath = os.path.join(root, file)
            destBlobClient = des_container_client.get_blob_client(fileName + filePath.replace(unZipTempPath,''))
            with open(filePath, "rb") as data:
                destBlobClient.upload_blob(data,overwrite=True)
    
    #remove all temp files 
    shutil.rmtree(unZipTempPath)
    os.remove(zipFilePath)

    return func.HttpResponse("done")

