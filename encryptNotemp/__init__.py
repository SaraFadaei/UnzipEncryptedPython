
import logging
import azure.functions as func
import io
import zipfile
from azure.storage.blob import BlobServiceClient, ContainerClient


storageAccountConnstr = "DefaultEndpointsProtocol=https;AccountName=stdataplatformddata;AccountKey=EyXLt2r/9dQnvlm9oIeBQBXt6UsLAdJVy6gYypKacJYHHmhe7Cj0JPdBBxbkTaadpIuk3Y8TVCt8+AStMv9f7w==;EndpointSuffix=core.windows.net"
container = "data-hub/powercurve/preprod/zip"
destcontainer = "data-hub/powercurve/preprod/unzip"

def main(req=func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    reqBody = req.get_json()
    fileName = reqBody['fileName']
    zipPass =  bytes(reqBody['password'],'utf-8')

    blob_service_client = BlobServiceClient.from_connection_string(storageAccountConnstr)
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(fileName)
    des_container_client = blob_service_client.get_container_client(destcontainer)

    with io.BytesIO() as b:
        download_stream = blob_client.download_blob(0)
        download_stream.readinto(b)
        with zipfile.ZipFile(b, compression=zipfile.ZIP_LZMA) as z:
            for filename in z.namelist():
                #if not filename.endswith('/'):
                    print(filename)
                    with z.open(filename, mode='r', pwd=zipPass) as f:
                        des_container_client.get_blob_client(
                            filename).upload_blob(f,overwrite=True)
                        
    return func.HttpResponse("done")